import { readFileSync } from 'node:fs';
import assert from 'node:assert/strict';
import test from 'node:test';

const source = readFileSync(new URL('../app/page.tsx', import.meta.url), 'utf8');

test('story and questions are preserved while opening qualifications are reduced', () => {
  const preserved = [
    "Two flats share a wall. Martin owns upstairs. Leah and Sam rent downstairs with their daughter, Mia. Damp appears behind Mia&apos;s bed and spreads while both households try to reach repair.",
    "Upstairs, Martin&apos;s managing-agent route reaches a person with authority. Downstairs, Leah and Sam enter a tenant portal designed to receive many requests; it gives them a reference number while Mia&apos;s room keeps changing.",
    "The upstairs wall is repaired. Downstairs, an inspection is offered after Leah and Sam have found another tenancy. They leave before anyone enters the room. The case can close; the consequences do not necessarily close with it.",
    "What had changed by the time an inspection was offered?",
    "What could each household actually reach while the same wall was changing?"
  ];
  for (const text of preserved) assert.ok(source.includes(text), text);

  const opening = source.split('<article className="concrete-story')[1].split('</article>')[0];
  assert.match(opening, /A composite scene from/);
  assert.match(opening, /<summary>Looking more closely<\/summary>/);
  assert.doesNotMatch(opening, /not a documented|efficacy|practical advantage|tested intervention|worked-revision/);
  assert.equal(source.split('href="/explore/worked-revision.html"').length - 1, 1);

  const caption = source.split('<p className="art-key">')[1].split('</p>')[0];
  assert.equal(caption, 'A shared fire, two different positions. A place to begin together without needing to share the same view.');
  assert.doesNotMatch(caption, /Why this is here|\b(?:us|our)\b/);

  assert.match(source, /Practical advantage over careful ordinary reasoning or established methods has not been demonstrated/);
});
