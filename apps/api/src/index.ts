import { Hono } from 'hono';

// The saves.fm API: one typed REST API for the web and mobile apps. Every
// public route lives under /v1 (see "Public-ready API" in docs/spec.md).
const app = new Hono();

const v1 = new Hono();
v1.get('/health', (c) => c.json({ ok: true, service: 'saves-api' }));

app.route('/v1', v1);
app.notFound((c) => c.json({ error: 'Not found' }, 404));

export default app;
