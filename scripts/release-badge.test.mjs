// The committed release badge and the app versions must match package.json.
// After bumping the version, run `pnpm badges` and commit docs/badges/release.svg.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { test } from 'node:test';

const root = new URL('../', import.meta.url);
const read = (path) => readFileSync(new URL(path, root), 'utf8');
const version = JSON.parse(read('package.json')).version;

test('release badge shows the package.json version', () => {
  const label = read('docs/badges/release.svg').match(/aria-label="release: ([^"]+)"/)?.[1];
  assert.equal(label, version === '0.0.0' ? 'none yet' : `v${version}`);
});

test('every app has the same version as the root', () => {
  for (const app of ['apps/web/package.json', 'apps/api/package.json']) {
    assert.equal(JSON.parse(read(app)).version, version, app);
  }
  const mobile = read('apps/mobile/pubspec.yaml').match(/^version: ([^+\s]+)/m)?.[1];
  assert.equal(mobile, version, 'apps/mobile/pubspec.yaml');
});
