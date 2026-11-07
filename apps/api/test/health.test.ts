import { describe, expect, it } from 'vitest';
import app from '../src/index';

describe('GET /v1/health', () => {
  it('reports the API is up', async () => {
    const res = await app.request('/v1/health');
    expect(res.status).toBe(200);
    expect(await res.json()).toEqual({ ok: true, service: 'saves-api' });
  });

  it('answers unknown routes with a JSON 404', async () => {
    const res = await app.request('/nope');
    expect(res.status).toBe(404);
    expect(await res.json()).toEqual({ error: 'Not found' });
  });
});
