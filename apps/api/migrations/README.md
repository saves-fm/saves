# D1 migrations

SQL migrations for the `DB` binding, applied in order by Wrangler. The core tables (users, passkeys, ra_links, verification_codes, games, achievements, unlocks, sessions) arrive in v0.2.0; the full model is in [docs/spec.md](../../../docs/spec.md#data-model-d1).

```bash
npx wrangler d1 migrations create DB <name>                 # new migration file
npx wrangler d1 migrations apply DB --local                 # local dev
npx wrangler d1 migrations apply DB --env staging --remote  # staging
```
