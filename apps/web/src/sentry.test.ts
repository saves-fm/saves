import { describe, expect, it } from 'vitest';
import { environmentFor } from './sentry';

describe('environmentFor', () => {
  it('tells previews, staging and production apart by hostname', () => {
    expect(environmentFor('pr-12-saves-web-staging.matthewsullivan21.workers.dev')).toBe('preview');
    expect(environmentFor('saves-web-staging.matthewsullivan21.workers.dev')).toBe('staging');
    expect(environmentFor('saves.fm')).toBe('production');
  });
});
