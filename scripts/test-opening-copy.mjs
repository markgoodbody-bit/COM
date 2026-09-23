import { readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import assert from 'node:assert/strict';
import test from 'node:test';

const source = readFileSync(new URL('../app/page.tsx', import.meta.url), 'utf8');
const baseline = execFileSync('git', ['show', 'ccf65dcc5780685608ce54ff4e6c888ac731611e:app/page.tsx'], {encoding: 'utf8'});
test('story and questions are preserved while opening qualifications are reduced', () => {
  const narrative = text => text.split('<div className="story-body">')[1].split('<p className="story-source">')[0];
  assert.equal(narrative(source), narrative(baseline));
  const opening = source.split('<article className="concrete-story')[1].split('</article>')[0];
  assert.match(opening, /A composite scene from/);
  assert.match(opening, /<summary>Looking more closely<\/summary>/);
  assert.doesNotMatch(opening, /not a documented|efficacy|practical advantage|tested intervention|worked-revision/);
  assert.equal(source.split('href="/explore/worked-revision.html"').length - 1, 1);
  const caption = source.split('<p className="art-key">')[1].split('</p>')[0];
  assert.doesNotMatch(caption, /Why this is here|\b(?:us|our)\b/);
  assert.match(source, /Practical advantage over careful ordinary reasoning or established methods has not been demonstrated/);
});
