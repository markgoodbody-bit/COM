"use strict";
const test=require("node:test");
const assert=require("node:assert/strict");
const E=require("../src/engine.js");

// A refused command must throw and leave the whole game state byte-identical.
function refused(g, act, pattern) {
  const before = JSON.stringify(g);
  assert.throws(act, pattern);
  assert.equal(JSON.stringify(g), before);
}

test("a fleet with no ships cannot move", () => {
  const g = E.createGame();
  g.fleets.iron.ships = [];
  refused(g, () => E.moveFleet(g, "directorate", "iron", "meridian"), /no ships/);
});

test("a ship without a positive speed cannot move its fleet", () => {
  const g = E.createGame();
  g.fleets.iron.ships[0].speed = 0;
  refused(g, () => E.moveFleet(g, "directorate", "iron", "meridian"), /positive speed/);
});

test("embarking is limited by the ships' troop capacity and the garrison", () => {
  const g = E.createGame();
  // iron: one ship with room for 16 troops, carrying 6; the cinder garrison holds 12.
  refused(g, () => E.embarkTroops(g, "directorate", "iron", 11), /capacity/);
  E.embarkTroops(g, "directorate", "iron", 10);
  assert.equal(g.fleets.iron.troops, 16);
  assert.equal(g.systems.cinder.garrison, 2);
  refused(g, () => E.embarkTroops(g, "directorate", "iron", 1), /capacity/);
  // wanderer: room for 10, carrying 4; the beacon garrison holds 12.
  refused(g, () => E.embarkTroops(g, "league", "wanderer", 13), /garrison/);
});

test("troops load, travel and land, and the total is conserved", () => {
  const g = E.createGame();
  const total = () => g.systems.cinder.garrison + g.fleets.iron.troops;
  const start = total();
  E.embarkTroops(g, "directorate", "iron", 4);
  assert.equal(total(), start);
  assert.equal(g.fleets.iron.troops, 10);
  E.moveFleet(g, "directorate", "iron", "meridian");
  E.tick(g, 2);
  assert.equal(g.fleets.iron.at, "meridian");
  const landing = E.invade(g, "directorate", "iron", "meridian");
  assert.equal(landing.success, true);
  assert.equal(landing.assault, 30); // 10 troops x 3, no commander aboard
  assert.equal(g.systems.meridian.owner, "directorate");
  assert.equal(g.fleets.iron.troops, 0);
});

test("troops disembark into a friendly garrison only", () => {
  const g = E.createGame();
  E.disembarkTroops(g, "directorate", "iron", 2);
  assert.equal(g.fleets.iron.troops, 4);
  assert.equal(g.systems.cinder.garrison, 14);
  E.moveFleet(g, "directorate", "iron", "meridian");
  E.tick(g, 2);
  assert.equal(g.systems.meridian.owner, null);
  refused(g, () => E.disembarkTroops(g, "directorate", "iron", 1), /friendly/);
  refused(g, () => E.embarkTroops(g, "directorate", "iron", 1), /friendly/);
});

test("bad troop commands change nothing", () => {
  const g = E.createGame();
  for (const bad of [0, -3, 1.5, "4", null]) {
    refused(g, () => E.embarkTroops(g, "directorate", "iron", bad), /positive integer/);
    refused(g, () => E.disembarkTroops(g, "directorate", "iron", bad), /positive integer/);
  }
  refused(g, () => E.disembarkTroops(g, "directorate", "iron", 7), /aboard/);
  refused(g, () => E.embarkTroops(g, "league", "iron", 1), /not controlled/);
  refused(g, () => E.embarkTroops(g, "directorate", "nosuch", 1), /not controlled/);
  E.moveFleet(g, "directorate", "iron", "meridian");
  refused(g, () => E.embarkTroops(g, "directorate", "iron", 1), /transit/);
  refused(g, () => E.disembarkTroops(g, "directorate", "iron", 1), /transit/);
});

test("the same seed and troop orders reproduce byte-identical games", () => {
  function run() {
    const g = E.createGame(7);
    E.embarkTroops(g, "league", "wanderer", 6);
    E.moveFleet(g, "league", "wanderer", "farpoint");
    E.tick(g, 1);
    E.invade(g, "league", "wanderer", "farpoint");
    return JSON.stringify(g);
  }
  assert.equal(run(), run());
});
