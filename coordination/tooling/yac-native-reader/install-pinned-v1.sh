#!/usr/bin/env bash
# Mechanical Ethics / Framework-Lab — exact YAC native reader toolchain.
# Purpose: one normal, non-root, lockfile-frozen npm installation ONLY.
# No Wrangler execution, authentication, provider contact or public deployment.
set -Eeuo pipefail

usage() {
  printf 'Usage: %s --repo /absolute/path/to/yac-source (--check | --install)\n' "$0" >&2
  exit 64
}

repo=''
mode=''
while (($#)); do
  case "$1" in
    --repo) (($# >= 2)) || usage; repo=$2; shift 2 ;;
    --check|--install) [[ -z $mode ]] || usage; mode=$1; shift ;;
    *) usage ;;
  esac
done
[[ -n $repo && -n $mode && $repo == /* ]] || usage
[[ $(id -u) -ne 0 ]] || { echo 'REFUSED_ROOT: run as restricted ordinary development account' >&2; exit 65; }
[[ -d $repo/v1 && -f $repo/v1/package.json && -f $repo/v1/package-lock.json ]] || {
  echo 'MISSING_PINNED_V1_SOURCE'; exit 66;
}
[[ ! -L $repo/v1 && ! -L $repo/v1/node_modules ]] || {
  echo 'REFUSED_SYMLINK_V1_OR_MODULES'; exit 66;
}
[[ ! -f $repo/.npmrc && ! -f $repo/v1/.npmrc ]] || {
  echo 'REFUSED_PROJECT_NPMRC: unexpected project registry/auth config'; exit 65;
}
for k in CLOUDFLARE_API_TOKEN CLOUDFLARE_API_KEY CF_API_KEY NPM_TOKEN NODE_AUTH_TOKEN; do
  if [[ -v "$k" && -n ${!k} ]]; then
    echo "REFUSED_CREDENTIAL_ENV: ${k} is set (contents not read)" >&2; exit 65
  fi
done
command -v node >/dev/null && command -v npm >/dev/null && command -v git >/dev/null || {
  echo 'MISSING_NODE_NPM_OR_GIT'; exit 66;
}
node -e 'const major=+process.versions.node.split(".")[0]; if(major<22) {console.error("NEEDS_NODE_22_OR_NEWER"); process.exit(66)}'

# Pin exact package metadata to the accepted PR134 source; not to a mutable tag.
expected_pkg='bbde5af13814d687e7233f977b5f2111a02f85be'
expected_lock='91a2b03e403fdc6f387c00ec636d4d290a347b6e'
actual_pkg=$(git hash-object "$repo/v1/package.json")
actual_lock=$(git hash-object "$repo/v1/package-lock.json")
[[ $expected_pkg == "$actual_pkg" && $expected_lock == "$actual_lock" ]] || {
  echo 'LOCK_OR_PACKAGE_BYTES_CHANGED: do not install until re-reviewed' >&2; exit 67;
}

node - "$repo/v1" <<'JS'
const fs=require('node:fs');
const base=process.argv[2];
const pkg=JSON.parse(fs.readFileSync(base+'/package.json', 'utf8'));
const lock=JSON.parse(fs.readFileSync(base+'/package-lock.json', 'utf8'));
const expected = {
 'wrangler':'4.143.1', 'workerd':'1.20260926.1',
 'miniflare':'5.20260926.1-alpha',
 '@cloudflare/workerd-linux-64':'1.20260926.1'
};
function fail(reason) {console.error('LOCK_VALIDATION_STOP: '+reason); process.exit(67)}
if(lock.lockfileVersion!==3) fail('LOCKFILE_FORMAT');
if(pkg.devDependencies?.wrangler!==expected.wrangler ||
   lock.packages?.['']?.devDependencies?.wrangler!==expected.wrangler) fail('ROOT_WRANGLER_PIN');
for(const [name,version] of Object.entries(expected)) {
 const p=lock.packages?.['node_modules/'+name];
 if(!p || p.version!==version) fail('DEPENDENCY_PIN_'+name);
}
for(const [name,p] of Object.entries(lock.packages||{})) {
 if (!name || !p.resolved) continue;
 if (!p.resolved.startsWith('https://registry.npmjs.org/')) fail('NON_NPM_REGISTRY_'+name);
 if (typeof p.integrity!=='string' || !p.integrity.startsWith('sha512-')) fail('MISSING_INTEGRITY_'+name);
}
console.log('PINNED_PACKAGE_LOCK_OK / 4.143.1 / 1.20260926.1 / 5.20260926.1-alpha');
JS

if [[ $mode == --install ]]; then
  [[ ! -e $repo/v1/node_modules ]] || {
    echo 'REFUSED_EXISTING_MODULES: npm ci would erase this directory'; exit 65;
  }
  tmp=$(mktemp -d /tmp/yac-locked-npm.XXXXXXXX)
  trap 'rm -rf -- "$tmp"' EXIT
  : > "$tmp/empty-npmrc"
  : > "$tmp/empty-global-npmrc"
  export NPM_CONFIG_USERCONFIG="$tmp/empty-npmrc"
  export NPM_CONFIG_GLOBALCONFIG="$tmp/empty-global-npmrc"
  export NPM_CONFIG_CACHE="$tmp/cache"
  export NPM_CONFIG_AUDIT=false NPM_CONFIG_FUND=false
  export NPM_CONFIG_IGNORE_SCRIPTS=true
  export NPM_CONFIG_UPDATE_NOTIFIER=false
  echo 'INSTALL_START: isolated npm ci; lifecycle scripts disabled; official locked npm registry URLs only'
  ( cd "$repo/v1" && npm ci --ignore-scripts --no-audit --no-fund --fetch-retries=0 --fetch-timeout=20000 \
      --registry=https://registry.npmjs.org/ )
fi

if [[ ! -d $repo/v1/node_modules ]]; then
  echo 'NOT_INSTALLED: no local node_modules; run with --install (one controlled operation)'; exit 68
fi

node - "$repo/v1" <<'JS'
const fs=require('node:fs');
const base=process.argv[2];
const pins={wrangler:'4.143.1',workerd:'1.20260926.1',miniflare:'5.20260926.1-alpha',
  '@cloudflare/workerd-linux-64':'1.20260926.1'};
for (const [name,want] of Object.entries(pins)) {
  const p=base+'/node_modules/'+name+'/package.json';
  if(!fs.existsSync(p)) {console.error('MISSING_INSTALLED_PACKAGE '+name);process.exitCode=69;continue}
  const actual=JSON.parse(fs.readFileSync(p,'utf8')).version;
  if(actual!==want) {console.error('PIN_MISMATCH '+name+'='+actual);process.exitCode=69}
  else console.log('PACKAGE_PRESENT '+name+'@'+actual);
}
JS
printf 'NODE=%s NPM=%s\n' "$(node --version)" "$(npm --version)"
if [[ -d $repo/v1/node_modules/@cloudflare/workerd-linux-64 ]]; then
  find "$repo/v1/node_modules/@cloudflare/workerd-linux-64" -maxdepth 3 -type f -name workerd -exec sha256sum {} \;
fi
printf 'LOCKED_USERLAND_TOOLS_PRESENT; NO_RUNTIME_TEST / NO_PROVIDER_CALL / NO_DEPLOY\n'
