"use strict";
/* Frontier Ledger visual client: plain browser JavaScript, no libraries or remote resources.
   Every game or save string reaches the page through textContent, never as HTML.
   The local server's engine decides every action; this file only offers the choices the
   engine's own rules allow, and explains the ones it would refuse. */

const COSTS = { patrol: 14, troops: 6, mine: 10 };
const MISSIONS = ["diplomacy", "recon", "sabotage"];

const MISSION_LIMITS = "Diplomacy builds support; a neutral world may need several successful missions before joining. Support totals are not displayed. Recon currently only adds a world to the known chart, usually already done on arrival. It does not reveal enemy garrisons or facilities.";

function title(id) {
  return String(id).split("-").map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(" ");
}
function find(list, id) {
  return list.find(x => x.id === id) || null;
}
// An unknown system carries only id, x and y: its owner is never inferred.
function ownerClass(system, faction) {
  if (!system.known) return "unknown";
  if (system.owner === null) return "neutral";
  return system.owner === faction ? "own" : "enemy";
}
const OWNER_TEXT = { unknown: "Unknown", neutral: "Neutral", own: "Yours", enemy: "Enemy" };
function ownerText(system, faction) {
  return OWNER_TEXT[ownerClass(system, faction)];
}
// Chart coordinates to SVG units, keeping the chart's proportions; y grows downward in both.
function layout(systems, width = 600, height = 520, pad = 60) {
  const xs = systems.map(s => s.x), ys = systems.map(s => s.y);
  const minX = Math.min(...xs), minY = Math.min(...ys);
  const k = Math.min((width - 2 * pad) / Math.max(1, Math.max(...xs) - minX),
                     (height - 2 * pad) / Math.max(1, Math.max(...ys) - minY));
  return Object.fromEntries(systems.map(s => [s.id, { x: pad + (s.x - minX) * k, y: pad + (s.y - minY) * k }]));
}
function systemName(view, id) {
  return id ? title(id) : "nowhere";
}
function where(view, agent) {
  if (agent.fleet) {
    const f = find(view.fleets, agent.fleet);
    if (f && f.moving) return "aboard " + title(f.id) + ", travelling to " + title(f.moving.destination);
    return "aboard " + title(agent.fleet) + (f && f.at ? " at " + title(f.at) : "");
  }
  return "on " + systemName(view, agent.at);
}

function action(group, verb, args, label, enabled, reason) {
  return { group, verb, args, label, enabled, reason: enabled ? "" : reason };
}

// The choices for one selection. Each entry: {group, verb, args, label, enabled, reason}, and optionally
// {input:{kind:"count"|"select", ...}, argsFor(value)} when the player picks a number or a target first.
function actionsFor(view, sel) {
  const out = [], faction = view.faction;
  const over = view.winner ? "The campaign is over" : "";
  const sys = sel.system ? find(view.systems, sel.system) : null;
  const fleet = sel.fleet ? find(view.fleets, sel.fleet) : null;
  const agent = sel.agent ? find(view.agents, sel.agent) : null;

  if (fleet) {
    const here = fleet.at ? find(view.systems, fleet.at) : null;
    const name = title(fleet.id);
    if (fleet.moving) {
      out.push(action("Fleet", "move", [], name + " is travelling", false,
        "Arrives at " + title(fleet.moving.destination) + " in " + fleet.moving.daysLeft + " day(s)"));
    } else {
      const targets = view.systems.filter(s => s.id !== fleet.at);
      const preset = sys && sys.id !== fleet.at ? sys.id : targets[0].id;
      out.push({ group: "Fleet", verb: "move", label: "Send " + name + " to",
        enabled: !over && fleet.ships > 0,
        reason: over || (fleet.ships > 0 ? "" : "This fleet has no ships"),
        input: { kind: "select", value: preset,
          options: targets.map(s => ({ value: s.id, label: title(s.id) + " (" + ownerText(s, faction) + ")" })) },
        argsFor: v => [fleet.id, v], args: [fleet.id, preset] });
      const friendly = here && here.known && here.owner === faction;
      const room = fleet.capacity - fleet.troops;
      if (friendly) {
        const load = Math.min(room, here.garrison);
        out.push({ group: "Troops", verb: "loadtroops", label: "Load troops onto " + name,
          enabled: !over && load >= 1,
          reason: over || (room < 1 ? "The fleet is full" : "No garrison troops here to load"),
          input: { kind: "count", min: 1, max: Math.max(1, load), value: Math.max(1, load) },
          argsFor: v => [fleet.id, String(v)], args: [fleet.id, String(Math.max(1, load))] });
        out.push({ group: "Troops", verb: "unloadtroops", label: "Unload troops into the garrison",
          enabled: !over && fleet.troops >= 1, reason: over || "No troops aboard",
          input: { kind: "count", min: 1, max: Math.max(1, fleet.troops), value: Math.max(1, fleet.troops) },
          argsFor: v => [fleet.id, String(v)], args: [fleet.id, String(Math.max(1, fleet.troops))] });
      } else if (here) {
        const commanders = fleet.agents.filter(id => find(view.agents, id));
        out.push({ group: "Troops", verb: "invade", label: "Invade " + title(here.id) + " with all troops",
          enabled: !over && fleet.troops >= 1,
          reason: over || "No troops aboard: load them at one of your worlds",
          input: commanders.length ? { kind: "select", value: "",
            options: [{ value: "", label: "No commander" }].concat(commanders.map(id => ({ value: id, label: "Led by " + title(id) }))) } : null,
          argsFor: v => v ? [fleet.id, here.id, v] : [fleet.id, here.id], args: [fleet.id, here.id] });
      }
      for (const id of fleet.agents) {
        out.push(action("Passengers", "leave", [id], "Disembark " + title(id) + " at " + title(fleet.at), !over, over));
      }
    }
  }

  if (agent) {
    const name = title(agent.id);
    if (agent.busy) {
      out.push(action("Agent", "mission", [], name + " is on a mission", false, "Advance days to see the result"));
    } else if (agent.fleet) {
      const f = find(view.fleets, agent.fleet);
      const docked = f && !f.moving && f.at;
      out.push(action("Agent", "leave", [agent.id], "Disembark " + name, !over && Boolean(docked),
        over || "The fleet is travelling; wait until it arrives"));
    } else if (agent.at) {
      const place = find(view.systems, agent.at);
      for (const f of view.fleets.filter(f => f.at === agent.at && !f.moving)) {
        out.push(action("Agent", "board", [agent.id, f.id], "Board " + title(f.id),
          !over && f.agents.length < f.agentSlots, over || "No free berth aboard " + title(f.id)));
      }
      for (const kind of MISSIONS) {
        const hostile = place && place.known && place.owner !== null && place.owner !== faction;
        const ok = kind !== "sabotage" || hostile;
        out.push(action("Missions", "mission", [agent.id, kind, agent.at],
          title(kind) + " on " + title(agent.at), !over && ok,
          over || "Sabotage needs an enemy world; " + title(agent.at) + " is " + ownerText(place, faction).toLowerCase()));
      }
      if (agent.power) {
        for (const c of view.agents.filter(c => c.id !== agent.id && c.at === agent.at && !c.fleet && !c.busy && !c.power)) {
          out.push(action("Agent", "awaken", [agent.id, c.id], "Awaken " + title(c.id) + "'s hidden potential",
            !over, over));
        }
      }
    }
  }

  if (sys && sys.known && sys.owner === faction && !fleet && !agent) {
    for (const type of Object.keys(COSTS)) {
      const cost = COSTS[type], yard = sys.facilities && sys.facilities.yard > 0;
      const ok = view.treasury >= cost && (type !== "patrol" || yard);
      const why = type === "patrol" && !yard ? "Patrol ships need a shipyard here"
        : "Costs " + cost + "; you have " + view.treasury;
      out.push(action("Build at " + title(sys.id), "build", [sys.id, type],
        "Build " + (type === "troops" ? "troops (+3 garrison)" : type === "mine" ? "a mine" : "a patrol ship") + " for " + cost,
        !over && ok, over || why));
    }
  }
  for (const a of out) if (a.enabled) a.reason = "";
  return out;
}

// The event lines added since `before`; the list holds only the last 20, so match its old newest line.
function newEvents(before, after) {
  const i = after.lastIndexOf(before[before.length - 1]);
  return i < 0 ? after.slice() : after.slice(i + 1);
}

// What changed, in words, for the message line after an accepted action.
function describe(verb, args, view) {
  const t = args.map(title);
  switch (verb) {
    case "board": return t[0] + " boarded " + t[1] + ".";
    case "leave": return t[0] + " disembarked.";
    case "move": return t[0] + " set out for " + t[1] + ".";
    case "mission": return t[0] + " began a " + args[1] + " mission on " + t[2] + ".";
    case "loadtroops": return "Loaded " + args[1] + " troops onto " + t[0] + ".";
    case "unloadtroops": return "Unloaded " + args[1] + " troops from " + t[0] + ".";
    case "build": return "Started building " + args[1] + " at " + t[0] + ".";
    case "invade": return t[0] + " committed its entire landing force at " + t[1] + ". See the events for the result.";
    case "awaken": return t[0] + " awakened " + t[1] + "'s potential.";
    case "tick": return "Advanced to day " + view.day + ".";
    default: return "Done.";
  }
}

// The four requests of GUI-BRIDGE.md v1. base is "" in the browser; tests pass a loopback origin.
function createApi(base = "", fetchImpl = fetch, extraHeaders = {}) {
  let csrf = null, revision = null;
  async function reply(r) {
    let body = null;
    try { body = await r.json(); } catch { body = null; }
    if (!r.ok || !body) {
      const err = new Error((body && body.error) || "The game server did not answer (" + r.status + ")");
      err.status = r.status;
      throw err;
    }
    if (body.csrf) csrf = body.csrf;
    if (typeof body.revision === "number") revision = body.revision;
    return body;
  }
  async function post(route, fields) {
    const r = await fetchImpl(base + route, { method: "POST",
      headers: { "Content-Type": "application/json", "X-Frontier-CSRF": csrf, ...extraHeaders },
      body: JSON.stringify({ revision, ...fields }) });
    return reply(r);
  }
  return {
    state: async () => reply(await fetchImpl(base + "/api/state")),
    action: (verb, args) => post("/api/action", { verb, args }),
    newGame: (seed, faction) => post("/api/new", { seed, faction }),
    save: () => post("/api/save", {}),
    load: save => post("/api/load", { save }),
  };
}

/* ---------- Browser side ---------- */

function el(tag, cls, text) {
  const node = document.createElement(tag);
  if (cls) node.className = cls;
  if (text !== undefined) node.textContent = text;
  return node;
}
function svg(tag, attrs, text) {
  const node = document.createElementNS("http://www.w3.org/2000/svg", tag);
  for (const [k, v] of Object.entries(attrs || {})) node.setAttribute(k, String(v));
  if (text !== undefined) node.textContent = text;
  return node;
}
function facts(pairs) {
  const dl = el("dl", "facts");
  for (const [k, v] of pairs) { dl.append(el("dt", "", k), el("dd", "", v)); }
  return dl;
}

function startApp() {
  const $ = id => document.getElementById(id);
  const api = createApi();
  let view = null, sel = { system: null, fleet: null, agent: null }, busy = false, unsaved = false;

  function say(text) { $("message").textContent = text; $("error").textContent = ""; }
  function fail(err) { $("error").textContent = err.message || String(err); }

  async function run(work) {
    if (busy) return;
    busy = true;
    document.body.classList.add("waiting");
    try { await work(); }
    catch (err) {
      if (err.status === 409) {
        try { view = (await api.state()).view; render(); } catch { /* the error below still shows */ }
        fail(new Error("The campaign changed elsewhere, so the map was refreshed. Please choose again."));
      } else fail(err);
    } finally { busy = false; document.body.classList.remove("waiting"); }
  }
  async function act(verb, args) {
    await run(async () => {
      const r = await api.action(verb, args);
      const before = view.events;
      view = r.view; unsaved = true;
      if (sel.fleet && !find(view.fleets, sel.fleet)) sel.fleet = null;
      render();
      // After days pass, show what happened right away; the full list stays below the chart.
      const fresh = verb === "tick" ? newEvents(before, view.events) : [];
      say([describe(verb, args, view)].concat(fresh.slice(-4), fresh.length > 4 ? ["(" + (fresh.length - 4) + " more below the chart)"] : []).join("\n"));
    });
  }

  function select(next) {
    sel = { system: null, fleet: null, agent: null, ...next };
    render();
  }

  function renderStats() {
    const box = $("stats");
    box.replaceChildren();
    const rows = [["Day", String(view.day)], ["Side", view.factionName], ["Treasury", String(view.treasury)],
      ["Worlds", String(view.controlled)]];
    if (view.winner) rows.push(["Winner", view.winner === view.faction ? "You" : title(view.winner)]);
    for (const [k, v] of rows) {
      const d = el("div", k === "Winner" ? "winner" : "");
      d.append(el("dt", "", k), el("dd", "", v));
      box.append(d);
    }
  }

  function renderChart() {
    const chart = $("chart"), pos = layout(view.systems);
    const focused = document.activeElement && document.activeElement.getAttribute
      ? document.activeElement.getAttribute("data-system") : null;
    chart.replaceChildren();
    const moving = sel.fleet && find(view.fleets, sel.fleet);
    const destination = moving && moving.moving ? moving.moving.destination : null;
    for (const s of view.systems) {
      const p = pos[s.id], cls = ownerClass(s, view.faction);
      const g = svg("g", { class: "star " + cls + (sel.system === s.id ? " selected" : "") + (destination === s.id ? " destination" : ""),
        transform: "translate(" + p.x.toFixed(1) + " " + p.y.toFixed(1) + ")", tabindex: 0, role: "button",
        "data-system": s.id, "aria-pressed": sel.system === s.id ? "true" : "false",
        "aria-label": title(s.id) + ", " + ownerText(s, view.faction) + ", chart position " + s.x + "," + s.y });
      g.append(svg("circle", { class: "halo", r: 24 }), svg("circle", { class: "body", r: 12 }),
        svg("text", { class: "name", y: -22 }, title(s.id)), svg("text", { class: "owner", y: 32 }, ownerText(s, view.faction)));
      g.addEventListener("click", () => select({ system: s.id, fleet: keepFleet(s.id) }));
      g.addEventListener("keydown", e => {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); select({ system: s.id, fleet: keepFleet(s.id) }); }
      });
      chart.append(g);
    }
    // Your docked fleets sit beside their star; a travelling fleet is drawn as a ring on its destination.
    const docked = {};
    for (const f of view.fleets) {
      if (f.at) {
        // Right of the star, clear of its name above and its owner below.
        const p = pos[f.at], i = (docked[f.at] = (docked[f.at] || 0) + 1) - 1;
        const x = p.x + 34 + i * 18, y = p.y;
        chart.append(svg("polygon", { class: "fleet-mark", points: [x, y - 7, x + 7, y, x, y + 7, x - 7, y].join(" ") }));
        const others = view.fleets.filter(o => o.at === f.at).length > 1 ? " +" : "";
        if (i === 0) chart.append(svg("text", { class: "fleet-label", x: x + 11, y: y + 4 }, title(f.id) + others));
      } else if (f.moving) {
        const p = pos[f.moving.destination];
        chart.append(svg("circle", { class: "transit", cx: p.x.toFixed(1), cy: p.y.toFixed(1), r: 34 }));
      }
    }
    if (focused) {
      const again = Array.from(chart.children).find(node => node.getAttribute("data-system") === focused);
      if (again) again.focus();
    }
  }
  // Keep a docked fleet selected when the player clicks another star: that star becomes its travel target.
  function keepFleet(systemId) {
    const f = sel.fleet && find(view.fleets, sel.fleet);
    return f && !f.moving && f.at !== systemId ? f.id : null;
  }

  function unitButton(label, chosen, onClick) {
    const b = el("button", chosen ? "selected" : "", label);
    b.type = "button";
    b.setAttribute("aria-pressed", chosen ? "true" : "false");
    b.addEventListener("click", onClick);
    return b;
  }

  function renderSelection() {
    const box = $("selection");
    box.replaceChildren();
    const sys = sel.system && find(view.systems, sel.system);
    const fleet = sel.fleet && find(view.fleets, sel.fleet);
    const agent = sel.agent && find(view.agents, sel.agent);
    if (!sys && !fleet && !agent) {
      box.append(el("p", "hint", "Click a star on the chart, or one of your fleets or agents below."));
      return;
    }
    if (sys) {
      const cls = ownerClass(sys, view.faction);
      box.append(el("h3", "", title(sys.id)));
      const rows = [["Owner", ownerText(sys, view.faction)], ["Position", sys.x + ", " + sys.y]];
      if (cls === "own") {
        rows.push(["Garrison", String(sys.garrison)],
          ["Facilities", "mine " + sys.facilities.mine + ", shipyard " + sys.facilities.yard + ", fort " + sys.facilities.fort]);
      } else if (cls === "unknown") {
        rows.push(["Status", "Not yet visited; send a ship to learn who holds it"]);
      } else {
        rows.push(["Garrison", "Not visible to you"]);
      }
      box.append(facts(rows));
      const fleets = view.fleets.filter(f => f.at === sys.id), agents = view.agents.filter(a => a.at === sys.id);
      if (fleets.length || agents.length) {
        const list = el("ul", "units");
        for (const f of fleets) {
          const li = el("li");
          li.append(unitButton("Fleet " + title(f.id) + ": " + f.troops + "/" + f.capacity + " troops",
            sel.fleet === f.id, () => select({ system: sys.id, fleet: f.id })));
          list.append(li);
        }
        for (const a of agents) {
          const li = el("li");
          li.append(unitButton("Agent " + title(a.id) + (a.busy ? " (on a mission)" : ""), sel.agent === a.id,
            () => select({ system: sys.id, agent: a.id })));
          list.append(li);
        }
        box.append(el("p", "hint", "Here:"), list);
      }
    }
    if (fleet) {
      box.append(el("h3", "", "Fleet " + title(fleet.id)));
      box.append(facts([
        ["Location", fleet.moving ? "Travelling to " + title(fleet.moving.destination) + ", " + fleet.moving.daysLeft + " day(s) left" : title(fleet.at)],
        ["Ships", String(fleet.ships)], ["Troops", fleet.troops + " of " + fleet.capacity],
        ["Passengers", fleet.agents.length ? fleet.agents.map(title).join(", ") : "none"],
        ["Berths", fleet.agents.length + " of " + fleet.agentSlots + " used"]]));
      if (sys && sys.id !== fleet.at && !fleet.moving) {
        box.append(el("p", "hint", "Selected destination: " + title(sys.id) + ". Use the Send button below."));
      }
    }
    if (agent) {
      box.append(el("h3", "", "Agent " + title(agent.id)));
      box.append(el("p", "hint", MISSION_LIMITS));
      box.append(facts([
        ["Where", where(view, agent)], ["Status", agent.busy ? "On a mission" : "Ready"],
        ["Skills", "diplomacy " + agent.skills.diplomacy + ", espionage " + agent.skills.espionage + ", command " + agent.skills.command],
        ["Potential", agent.power ? title(agent.power.kind) + " level " + agent.power.level : "None revealed"]]));
    }
  }

  function renderActions() {
    const box = $("actions");
    box.replaceChildren();
    const list = actionsFor(view, sel);
    if (!list.length) {
      box.append(el("p", "hint", sel.system || sel.fleet || sel.agent
        ? "Nothing to do here. Select one of your fleets or agents, or one of your worlds to build."
        : "Select something to see what you can do."));
      return;
    }
    let group = null, section = null, n = 0;
    for (const a of list) {
      if (a.group !== group) {
        group = a.group;
        section = el("div", "group");
        section.append(el("h3", "", group));
        box.append(section);
      }
      const row = el("div", "row"), id = "act-" + (n++);
      let control = null;
      if (a.input && a.input.kind === "count") {
        control = el("input");
        control.type = "number"; control.min = String(a.input.min); control.max = String(a.input.max);
        control.value = String(a.input.value); control.setAttribute("aria-label", "Number of troops");
      } else if (a.input && a.input.kind === "select") {
        control = el("select");
        control.setAttribute("aria-label", a.verb === "move" ? "Destination" : "Commander");
        for (const o of a.input.options) {
          const opt = el("option", "", o.label);
          opt.value = o.value;
          control.append(opt);
        }
        control.value = a.input.value;
      }
      const b = el("button", a.verb === "tick" ? "primary" : "", a.label);
      b.type = "button";
      b.disabled = !a.enabled;
      b.setAttribute("data-verb", a.verb);
      if (control) { control.disabled = !a.enabled; row.append(b, control); } else row.append(b);
      if (!a.enabled && a.reason) {
        const why = el("span", "reason", a.reason);
        why.id = id;
        b.setAttribute("aria-describedby", id);
        row.append(why);
      }
      b.addEventListener("click", () => act(a.verb, control && a.argsFor ? a.argsFor(control.value) : a.args));
      section.append(row);
    }
  }

  function renderUnits() {
    const fl = $("fleet-list"), al = $("agent-list");
    fl.replaceChildren(); al.replaceChildren();
    for (const f of view.fleets) {
      const li = el("li");
      li.append(unitButton(title(f.id) + " — " + (f.moving ? "to " + title(f.moving.destination) + " (" + f.moving.daysLeft + "d)" : "at " + title(f.at)),
        sel.fleet === f.id, () => select({ system: f.at || null, fleet: f.id })));
      fl.append(li);
    }
    for (const a of view.agents) {
      const li = el("li");
      li.append(unitButton(title(a.id) + " — " + where(view, a) + (a.busy ? ", on a mission" : ""), sel.agent === a.id,
        () => select({ system: a.at || null, agent: a.id })));
      al.append(li);
    }
  }

  function renderEvents() {
    const box = $("events");
    box.replaceChildren();
    for (const line of view.events.slice().reverse()) {
      const cls = /WORLD_LOST/.test(line) ? "loss" : /ATTACK_REPELLED/.test(line) ? "held" : "";
      box.append(el("li", cls, line));
    }
  }

  function render() {
    renderStats(); renderChart(); renderSelection(); renderActions(); renderUnits(); renderEvents();
    for (const id of ["advance-1", "advance-many"]) $(id).disabled = Boolean(view.winner);
  }

  $("advance-1").addEventListener("click", () => act("tick", ["1"]));
  $("advance-many").addEventListener("click", () => {
    const n = Number($("advance-n").value);
    if (!Number.isInteger(n) || n < 1 || n > 30) { fail(new Error("Choose between 1 and 30 days.")); return; }
    act("tick", [String(n)]);
  });
  $("new-game").addEventListener("click", () => run(async () => {
    const seed = Number($("seed").value);
    if (!Number.isSafeInteger(seed) || seed < 0 || seed > 4294967295) throw new Error("The seed must be a whole number from 0 to 4294967295.");
    if (unsaved && !window.confirm("Start a new campaign? Unsaved progress in this one will be lost.")) return;
    view = (await api.newGame(seed, $("side").value)).view;
    unsaved = false; sel = { system: null, fleet: null, agent: null };
    render(); say("New campaign started: seed " + seed + ", " + view.factionName + ".");
  }));
  $("save-game").addEventListener("click", () => run(async () => {
    const r = await api.save();
    const url = URL.createObjectURL(new Blob([r.save], { type: "application/json" }));
    const a = el("a");
    a.href = url; a.download = r.filename;
    document.body.append(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 10000);
    unsaved = false;
    say("Download requested: " + r.filename + ". Check your browser downloads before closing; the game cannot confirm the file was saved.");
  }));
  $("load-game").addEventListener("change", e => run(async () => {
    const file = e.target.files && e.target.files[0];
    e.target.value = "";
    if (!file) return;
    if (file.size > 2000000) throw new Error("That file is too large to be a Frontier Ledger save.");
    if (unsaved && !window.confirm("Load " + file.name + "? Unsaved progress in this campaign will be lost.")) return;
    view = (await api.load(await file.text())).view;
    unsaved = false; sel = { system: null, fleet: null, agent: null };
    render(); say("Loaded " + file.name + ": day " + view.day + ", " + view.factionName + ".");
  }));

  run(async () => { view = (await api.state()).view; render(); say("Click a star or one of your units to begin."); });
}

if (typeof document !== "undefined") document.addEventListener("DOMContentLoaded", startApp);
if (typeof module !== "undefined") module.exports = { title, ownerClass, ownerText, layout, actionsFor, newEvents, describe, createApi, COSTS, MISSION_LIMITS };
