import { Hono } from 'hono';

// Bindings from wrangler.toml, plus secrets set with `wrangler secret put`
export type Bindings = {
  DB: D1Database; // users, unlocks, sessions, rollups (D1)
  CACHE: KVNamespace; // RA game and achievement metadata
  IMAGES: R2Bucket; // generated share images, cached badge art
  RA_WEB_API_KEY: string;
};

// The saves.fm API: one typed REST API for the web and mobile apps. Every
// public route lives under /v1 (see "Public-ready API" in docs/spec.md).
const app = new Hono<{ Bindings: Bindings }>();

const v1 = new Hono<{ Bindings: Bindings }>();
v1.get('/health', (c) => c.json({ ok: true, service: 'saves-api' }));

app.route('/v1', v1);
app.notFound((c) => c.json({ error: 'Not found' }, 404));

export default app;
