# Releasing

Every version has a milestone (v0.1.0, v0.2.0, …). A release is cut by pushing a tag; `release.yml` does the rest.

1. Close or move every open issue in the milestone.
2. Bump the version to `X.Y.Z` in `package.json`, `apps/web/package.json`, `apps/api/package.json` and `apps/mobile/pubspec.yaml` (keep the `+build` number there).
3. Run `pnpm badges` to regenerate `docs/badges/release.svg`. On the first release (v0.1.0), also swap the README's status badge for the release badge.
4. Run `pnpm test`. It checks that the release badge and every app match `package.json`.
5. Commit, push, then tag and push the tag:

   ```bash
   git tag vX.Y.Z && git push origin vX.Y.Z
   ```

`release.yml` then checks the tag matches `package.json`, publishes the GitHub release with generated notes, pushes a `release/vX.Y.Z` branch at the tag, and closes the milestone with links to the release, tag, branch and the commits since the previous version.
