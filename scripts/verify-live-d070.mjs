import {readFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';

const origin=(process.env.PSFH_LIVE_ORIGIN || 'https://pleasestartfromhere.com').replace(/\/$/,'');
const inventoryPath=process.argv[2] || 'out/resources/inventory.json';
const attempts=Number(process.env.PSFH_VERIFY_ATTEMPTS || 12);
const delayMs=Number(process.env.PSFH_VERIFY_DELAY_MS || 5000);

const sha256=bytes=>createHash('sha256').update(bytes).digest('hex');
const sleep=ms=>new Promise(resolve=>setTimeout(resolve,ms));
const inventory=JSON.parse(await readFile(inventoryPath,'utf8'));

const targets=[];
for(const project of inventory.projects || []){
  for(const file of project.files || []){
    for(const field of ['current','snapshot']){
      if(!file[field]) continue;
      const expected = field === 'snapshot' && file.snapshot_identity
        ? file.snapshot_identity.sha256
        : file.sha256;
      if (!expected) continue;
      targets.push({
        label:`${project.id}:${file.path}:${field}`,
        path:file[field],
        expected
      });
    }
  }
}

for(const path of ['/manifest.json','/resources/inventory.json','/llms.txt','/packet.md','/changes.md']){
  const local=await readFile('out'+path);
  targets.push({label:'public:'+path,path,expected:sha256(local)});
}

let lastErrors=[];
for(let attempt=1; attempt<=attempts; attempt++){
  const errors=[];
  for(const target of targets){
    try{
      const response=await fetch(origin+target.path,{
        cache:'no-store',
        headers:{'cache-control':'no-cache','pragma':'no-cache'}
      });
      if(!response.ok){
        errors.push(`${target.label}: HTTP ${response.status}`);
        continue;
      }
      const bytes=Buffer.from(await response.arrayBuffer());
      const actual=sha256(bytes);
      if(actual!==target.expected){
        errors.push(`${target.label}: sha256 ${actual} != ${target.expected}`);
      }
    }catch(error){
      errors.push(`${target.label}: ${error?.message || String(error)}`);
    }
  }
  if(errors.length===0){
    console.log(`LIVE_PSFH_D070_VERIFIED targets=${targets.length} attempt=${attempt}`);
    process.exit(0);
  }
  lastErrors=errors;
  console.error(`live verification attempt ${attempt}/${attempts} failed (${errors.length} target(s))`);
  if(attempt<attempts) await sleep(delayMs);
}

console.error('LIVE_PSFH_D070_VERIFY_FAILED');
for(const error of lastErrors) console.error(error);
process.exit(1);
