# saves.fm — Product & Technical Spec

Nov 6, 2026 · @Matthew Sullivan · Revised Nov 7, 2026

## Overview

saves.fm is a Last.fm-style history and stats app for RetroAchievements players. RA already records every unlock with a timestamp, which works a lot like a scrobble. saves.fm keeps that history over time and turns it into charts, game pages, comparisons, recommendations and a year-end recap, the way Last.fm does for music.

**Who it's for:** RetroAchievements players who want to look back at what they've played, compare with friends, and find what to play next.

**Principles**

- **Built for the community.** Free, open source, and respectful of RA's rate limits and guidelines.
- **Its own account.** A saves.fm account exists only for saves.fm. The only outside account it connects to is RetroAchievements, which supplies the data. There's no Last.fm or other third-party linking.
- **Users never share their API keys.** Ownership is verified through RA's motto method, and all API calls use the app's own key.
- **Same experience everywhere.** The web app and the Flutter mobile app share one design system and match screen for screen.
- **Pages people want to share.** Profiles and Rewind recaps load fast and look good when the link is posted.
- **Not affiliated.** saves.fm is an independent fan project, not affiliated with RetroAchievements. Last.fm is the inspiration for the experience, not an integration.

## Features

### MVP

- **Sign up and verify:** create an account, link and verify a RetroAchievements username, and run a full history backfill.
- **Profile:** a public profile page with recent unlocks, masteries and totals.
- **Charts:** top games, consoles and genres by week, month, year and all time. Softcore and hardcore unlocks count together by default, with a hardcore-only filter.
- **History:** a scrollable timeline of unlocks grouped into estimated play sessions, plus "on this day" looking back across years.

### Phase 2: Last.fm-style pages

- **Game pages:** like a Last.fm artist page, but for a game. Shows how many saves.fm users have played it, unlocks this week, the top players, and your own history with it.
- **Global charts:** the top games and consoles across all saves.fm users this week, with the risers and fallers.
- **Now playing:** shows what a user is currently playing on their profile and in friends' feeds, using RA's rich presence data. The User Profile endpoint returns RichPresenceMsg and LastGameID. Freshness comes from polling itself: if RichPresenceMsg changed between a user's last two profile checks, they're playing right now. The slower User Summary endpoint (which adds RichPresenceMsgDate) is only called occasionally, for cases the change check can't settle, such as a status that hasn't changed for a while.
- **Tags:** genre and community tags on games for browsing and charts, like Last.fm's artist tags.

### Phase 3: Player 2 (compatibility)

- Compare two users and get a compatibility score based on overlapping games, consoles and masteries.
- Shows the games you both love and the ones only one of you has played.
- Follow other users, with a feed of friends' masteries.

### Phase 4: Discovery

- **Recommendations:** "players who mastered what you mastered also played…", based on overlap between users.
- **Finder:** browse the RA catalog by console, genre, rough length and difficulty (estimated from how rare a set's unlocks are), plus started-but-unfinished sets.

### Phase 5: Rewind

- A shareable year-end recap: hardest unlocks, top consoles, busiest months, longest streaks, most-played game pages and your Player 2 match.
- Generated each December from stored history, with share cards sized for social posts.
- The first Rewind is realistically December 2027, since it depends on v0.1.0–v1.3.0. There's no 2026 Rewind.

### Later: nice-to-haves

- **Profile cards:** auto-updating embeds in SVG (GitHub READMEs, most sites), PNG (forums, Discord) and an HTML iframe embed for personal sites. Layouts: recently played, top consoles, current streak, latest mastery. Rendered by the share-image service, with short caching.
- **Home-screen widgets:** Now playing, Streak, and This week's top 3 games. Each one needs a small native extension (SwiftUI WidgetKit on iOS, Android's own widget code) fed by data the Flutter app shares, so plan for some native work per widget.
- **Milestones and throwbacks:**
  - Examples: "5 years ago today you mastered X", "1 unlock from beating Y", friends' masteries and goal progress.
  - Delivery: an always-on in-app notifications feed, opt-in mobile push (Firebase Cloud Messaging for Android, relaying to Apple's push service for iOS), and an opt-in weekly email digest.
  - Each channel and notification type has its own setting.
- **Yearly goals:** users can set goals for masteries or beaten games, points or unlocks, number of different consoles, or a custom list of specific games to finish. Progress shows on the profile and feeds into Rewind.
- **Lists:** user-curated game lists. Games are picked from the catalog, and titles come from fixed templates (e.g. "Best \_\_\_ for \_\_\_", filled from set menus of genres, consoles and audiences). There's no free text, so there's nothing to moderate.
- **Percentiles:** e.g. "top 5% of saves.fm players for Game Boy". Calculated only among public, tracked users, and shown by default. Each user can hide their own.
- **Discord bot:** opt-in, shipping after Player 2. It posts friends' masteries and Rewind highlights to a server, reusing the friends feed.
- **Changelog and status:** a public changelog generated from GitHub releases, and a simple status page showing the existing health metrics (polling, RA errors, email delivery).

### Community-inspired features

These come from what the RA community already builds and asks for: browser scripts, trackers like RetroTrack and RA Tracker, and Wrapped-style recaps elsewhere.

- **Activity heatmap:** a year-long, GitHub-style grid where each cell is a day's unlocks in the user's time zone. It respects the hardcore-only filter, and appears at the top of every profile, as a profile card layout, and as a Rewind card.
- **Want to Play sync:** shows the user's RA Want to Play list, read-only, with edits made on RA so there's one source of truth. The Finder uses it to rank suggestions.
- **Spoiler protection:** an account setting blurs the titles, descriptions and badges of locked achievements everywhere. Each one can be revealed with a tap or click.
- **Achievement of the Week:**
  - A home page card showing the current AotW and your progress on that game.
  - A notification when a new one is posted: in-app, plus opt-in push and digest.
  - An AotW history on your profile. RA's API only returns the current AotW, so saves.fm records each week from launch onward.
- **Retro Ratio:** RA's weighted "true points" divided by regular points, as a rough difficulty measure.
  - Where it shows: an overall stat on profiles, a per-game figure on game pages and in the Finder's difficulty filter, trends in charts, and a "toughest year" stat in Rewind.
  - It comes with a short explanation, and users can hide it.
- **Friends' mastery alerts:** when someone you follow masters or beats a game, you get an in-app alert, plus opt-in push. These can lag up to about 15 minutes because of polling. Your own unlocks don't trigger alerts, since the emulator already shows them.
- **Rewind extras:** days active and your longest streak, your rarest unlock with the % of players who have it, how your year compares to the average saves.fm user, and a month-by-month comparison with last year.
- **Watch apps (v2.0.0):**
  - **Apple Watch:** a native SwiftUI app (Flutter doesn't target watchOS) with a watch face complication for now playing or your streak, plus a small app showing recent unlocks.
  - **Wear OS:** a matching Kotlin/Compose app with a tile and a complication, for parity.
- **Home Assistant (with the public API):** a documented REST sensor configuration and a small example integration in the repo. The community can build further on the public API.

## Accounts and verification

### Sign-up

- **Registration:** the user enters an email address, confirms it with a one-time code, then creates a passkey (WebAuthn). There's no password, and no RA credentials go through saves.fm. Users can register more than one passkey, e.g. phone and laptop.
- **What email is for:** account notices only: outages, big changes, security alerts such as a new passkey being added, and policy updates. No marketing unless the user opts in. Users can change their email later, and the new address is verified the same way.
- After creating a passkey, the user enters their RetroAchievements username and goes through the motto check below.
- **Account recovery:** if someone loses every device with a passkey, they can recover in either of two ways: prove RA ownership again with a fresh motto code, or use a one-time recovery link sent to their verified email. Either way, they then register a new passkey. Every recovery sends a security alert to the email on file, and email recovery is rate-limited.
- Profiles are **public by default**, with a setting to make them private. Private profiles are left out of global charts, Player 2 and recommendations. Email addresses are never shown on profiles.

### RA ownership check (motto method)

RetroAchievements doesn't offer OAuth. Their standalone integration guide describes a motto-based check instead:

1. saves.fm generates a short one-time code, e.g. `sfm-7K2Q9X`.
2. The user pastes the code into their RA profile motto. The page links straight to RA's settings.
3. The user taps "Verify". The backend reads the profile through the Web API and checks that the motto contains the code.
4. On success, the RA account is linked and the user is told they can remove the code from their motto. Then backfill starts.

Codes expire after 30 minutes and are single-use. One RA account can be linked to only one saves.fm account, and re-linking needs a fresh verification.

## Architecture

### Overview

- **Web:** React + TypeScript (Vite), with server-rendered or prerendered pages for public profiles and Rewind recaps. That makes link previews (Open Graph images) and first loads fast. Hosted on Cloudflare.
- **Mobile:** Flutter for iOS and Android, matching the web app's screens.
- **API:** Hono on Cloudflare Workers, one typed REST API used by both clients.
- **Database:** Cloudflare D1 for users, links, unlocks, sessions and scrobbles.
- **Storage:** R2 for generated share images (Rewind cards, OG images) and cached badge art if needed.
- **Jobs:** Cron Triggers plus Cloudflare Queues for polling, backfills and stat rollups.
- **Cache:** KV, or the Cache API, for RA game and achievement metadata, which rarely changes.

### Keeping web and mobile matched

- **Shared design tokens:** one token source (Style Dictionary or a similar tool) defines colors, type scale, spacing, radius and motion. A build step generates CSS variables for the web and a Dart theme file for Flutter. Neither app hardcodes a value.
- **Shared API contract:** an OpenAPI schema generated from the Hono routes (e.g. via Zod schemas). The TypeScript client is generated for web and the Dart client for Flutter, so both apps get the same data in the same shape.
- **Screen parity checklist:** every feature ships on web first. Each feature issue notes what the mobile version needs, so the mobile milestone starts from a complete list. The apps release at full parity with web.
- **Keep the mobile pipeline alive before v2.0.0:** from v0.2.0, CI builds a minimal Flutter app that uses the generated Dart theme and Dart API client, with one golden test. Token and schema changes that break Dart fail the PR right away, instead of piling up until mobile work starts.
- **Shared logic lives on the server:** stats, session estimation, compatibility scores and recommendations are computed by the API. Both clients only render the results, so the numbers never drift between apps.

### Testing

- Unit tests for session estimation, chart rollups and compatibility scoring, using fixed fixtures.
- Contract tests against the OpenAPI schema for both generated clients.
- Recorded RA responses for integration tests, so CI never calls the live API.
- Golden or screenshot tests on key screens in both apps to catch drift between them.

### Repo and environments

- **One repo** for everything:
  - `apps/web`: React + Vite
  - `apps/mobile`: Flutter
  - `apps/api`: Hono on Workers
  - `packages/tokens`: design tokens, building CSS variables and a Dart theme
  - `packages/api-schema`: OpenAPI, plus the generated TypeScript and Dart clients
- **Tooling:** pnpm workspaces for the JavaScript side, Melos for Flutter. One PR can change the API and both clients together.
- **Environments:**
  - **Local:** Wrangler dev, with a local D1 and recorded RA fixtures by default.
  - **Staging:** its own Worker and D1 database, using the development RA key with a small set of test users. Every PR gets a preview deploy.
  - **Production:** its own Worker, D1 database, R2 bucket and RA key.

### Foundations built in from day one

- **Translation-ready:** English only at launch, but every string lives in translation files: ICU message format on web and Flutter's ARB files on mobile, generated from one shared source. Dates, numbers and plurals use locale-aware formatting. Adding a language later is translation work, not a refactor.
- **Themes:** light and dark at launch, following the system setting with a manual override. Themes are token sets in `packages/tokens`, so more themes (e.g. CRT or console-inspired) can ship later as supporter perks with no component changes. Every theme must pass the contrast checks.
- **Share-image service:** one Worker renders images with Satori (JSX to SVG) and resvg (SVG to PNG, via WASM). Fonts are bundled with it. Images are cached in R2 and keyed by content, so they re-render only when the data changes. It's used for profile link previews, masteries, Rewind cards and profile cards.
- **Public-ready API:** endpoints for public data are designed from the start as if they were public: versioned (`/v1`), documented in OpenAPI, with stable IDs, pagination and no internal-only fields. After launch, they open to third-party developers with API keys and per-key rate limits. Only public, tracked profiles are exposed, and nothing that goes through the saves.fm API ever hits RA directly.

## Data pipeline

### Backfill (on RA link)

1. Fetch the user's games with progress (`API_GetUserCompletionProgress`, paged).
2. Walk the user's unlock history in 30-day windows (`API_GetAchievementsEarnedBetween`) from their RA join date to now, and store it in `unlocks`. Any game whose stored unlock count doesn't match its progress is repaired from that game's per-user detail.
3. Fetch and cache metadata (title, console, genre, badge) for any games not already cached.
4. Run session estimation and stat rollups.

The exact calls are in the backfill recipe under the RetroAchievements API reference.

Backfills run through a queue at a steady, throttled rate. A large library can take a while to finish, and the UI shows progress ("Importing 214 of 640 games…") instead of blocking.

### Ongoing polling

- A Cron Trigger queues poll jobs.
- **Change-triggered polling:** each cycle makes one cheap `API_GetUserProfile` call per due user. Unlocks are fetched (`API_GetUserRecentAchievements`) only when `TotalPoints`, `TotalSoftcorePoints` or `TotalTruePoints` has changed since the last check. Any new unlock changes at least one of them, so this trigger is exact. `RichPresenceMsg` isn't used as the trigger: it changes constantly during play ("World 1-2, 3 lives"), which would mean an unlock fetch on almost every check. Presence and `LastGameID` still drive now playing and tier changes.
- **Fallback:** a full unlock check every 4 hours for active and weekly users, and daily for idle users, to catch anything a profile check missed (e.g. zero-point achievements, which don't change any points total).
- **Polling tiers:**
  - Active in the last 24 hours: profile check every 15 minutes
  - Active this week: hourly
  - Idle: daily
- A shared rate limiter in a single Durable Object enforces both a requests-per-second limit and a hard daily call cap across all workers. KV can't do this job: it's eventually consistent and allows only about one write per second per key, so counters would drift and overshoot the cap.
- When usage nears the daily cap, idle-tier intervals stretch first, then weekly-tier intervals. Active users are slowed last.
- After each poll that finds new unlocks, that user's stat rollups are updated.
- Global charts are recomputed on their own Cron Trigger (every 15–60 minutes, tunable), not after each poll, so D1 doesn't take a site-wide write on every user check.

### Request budget (planning estimate, 5,000 users)

This assumes 10% of users are active, 30% weekly and 60% idle, and that unlock fetches only happen when a points total changes (see change-triggered polling). These are the numbers to share with RA; check them against real usage after launch.

| Tier | Users | Profile checks/day | Unlock fetches/day |
| --- | --- | --- | --- |
| Active | 500 | 48,000 (every 15 min) | \~8,000 (\~10 on change + 6 fallback each) |
| Weekly | 1,500 | 36,000 (hourly) | \~9,000 (6 fallback each) |
| Idle | 3,000 | 3,000 (daily) | \~3,000 (1 each) |
| **Total** | **5,000** | **87,000** | **\~20,000** |

That's about 107,000 RA calls a day, averaging about 1.2 per second, plus backfills and metadata refreshes. The proposed daily cap is 120,000 calls, to be confirmed with RA. Backfills run in a separate, lower-priority queue that pauses when the cap is close. At 1,000 users the same model comes to about 21,000 calls a day.

### Rate limits and good behavior

- Cache all game and achievement metadata, and refresh it only when a set changes.
- Never call RA from a client request. Pages only read data that's already stored.
- Back off on errors and 429 responses. Alert if the error rate jumps.
- Contact RA staff before a public launch to describe the use case and expected request volume.

### Session estimation

- Sort a user's unlocks by time, and start a new session whenever two unlocks in the same game are more than 45 minutes apart (a starting default, tuned against Matthew's own history before launch).
- Estimated session time is the span from first to last unlock, plus a small padding at each end.
- RA's recently-played data can help refine sessions that have few unlocks.
- Sessions are labeled "estimated" everywhere in the UI.

### Time and time zones

- All timestamps are stored in UTC.
- Each user's time zone is detected from their device at sign-up and can be changed in settings. It's stored as `users.time_zone`, an IANA name like `America/Phoenix`.
- Days, weeks, streaks, charts and Rewind are all calculated in the user's time zone, so a late-night session counts on the day the user actually played it.
- Weeks start on Monday (ISO weeks, as Last.fm does).
- Global charts use UTC weeks so every user sees the same chart.

## Data model (D1)

| Table | Key columns | Notes |
| --- | --- | --- |
| users | id, email (unique), email\_verified\_at, is\_public, tracking\_paused, time\_zone, locale, theme, hide\_percentiles, spoiler\_protection, show\_retro\_ratio, created\_at | saves.fm account, used only for saves.fm; is\_public defaults to true |
| passkeys | id, user\_id, credential\_id, public\_key, sign\_count, transports, created\_at, last\_used\_at | WebAuthn credentials; several per user |
| ra\_links | user\_id, ra\_user\_id (ULID), ra\_username, ra\_untracked, verified\_at, last\_polled\_at, poll\_tier | One per user; ra\_user\_id is unique |
| verification\_codes | user\_id, code, purpose, expires\_at, used\_at | Motto and email codes; purpose is ra\_link, ra\_recovery or email\_verify. Emails go out through Cloudflare Email Service (see Email) |
| supporters | user\_id, source, tier, since, until | Donation and supporter-perk status |
| games | ra\_game\_id, title, console\_id, genre, icon\_url, updated\_at | Cached metadata |
| game\_tags | ra\_game\_id, tag | Genre and community tags |
| achievements | ra\_achievement\_id, ra\_game\_id, title, points, unlock\_rate | Cached; unlock\_rate is used for rarity and difficulty |
| unlocks | user\_id, ra\_achievement\_id, ra\_game\_id, unlocked\_at, hardcore\_unlocked\_at | Core history table; unique on (user\_id, ra\_achievement\_id). unlocked\_at is the first unlock in either mode; hardcore\_unlocked\_at is when it was earned in hardcore (null if softcore only, equal to unlocked\_at if earned in hardcore first). A later hardcore unlock of a softcore achievement updates hardcore\_unlocked\_at and leaves unlocked\_at alone |
| sessions | id, user\_id, ra\_game\_id, started\_at, ended\_at, unlock\_count | Estimated |
| presence | user\_id, ra\_game\_id, message, seen\_at | Latest "now playing" |
| follows | follower\_id, followee\_id, created\_at | For Player 2 and the friends feed |
| stats\_rollups | user\_id, period, period\_start, mode, payload\_json | Precomputed per-user charts; mode is all or hardcore |
| global\_charts | period, period\_start, mode, payload\_json | Precomputed site-wide charts, public profiles only |
| notifications | id, user\_id, kind, payload\_json, created\_at, read\_at | In-app feed: milestones, throwbacks, friends' masteries, goal progress |
| notification\_prefs | user\_id, kind, in\_app, push, email\_digest | Per-type, per-channel settings; push and digest default off |
| push\_tokens | id, user\_id, platform, fcm\_token, created\_at, last\_seen\_at | One per device; deleted on sign-out or delivery failure |
| goals | id, user\_id, year, kind, target, game\_ids\_json, created\_at | kind is masteries, beaten, points, unlocks, consoles or custom\_list; progress is computed from unlocks |
| lists | id, user\_id, title\_template, title\_slots\_json, created\_at, updated\_at | Titles come from fixed templates and menus only |
| list\_items | list\_id, ra\_game\_id, position | Ordered games in a list |
| api\_keys | id, owner\_user\_id, key\_hash, name, rate\_limit, created\_at, revoked\_at | For the post-launch public API; only hashes stored |
| want\_to\_play | user\_id, ra\_game\_id, synced\_at | Read-only mirror of the user's RA Want to Play list |
| aotw\_history | week\_start, ra\_achievement\_id, ra\_game\_id, recorded\_at | Recorded weekly from launch, since RA only returns the current AotW |

Indexes go on `unlocks(user_id, unlocked_at)`, `unlocks(user_id, hardcore_unlocked_at)`, `unlocks(ra_game_id, unlocked_at)` and `sessions(user_id, started_at)`. Those are the time-range queries the profile charts, game pages and global charts use. Default charts count by `unlocked_at`; the hardcore-only filter counts by `hardcore_unlocked_at`, so an upgraded unlock lands on the day it was actually earned in hardcore.

D1 has per-database size limits. If the unlocks table grows past them, the plan is to shard by user, or archive older raw rows to R2 and keep the rollups in D1.

## RetroAchievements API reference

All of saves.fm's data comes from the RetroAchievements Web API ([full docs](https://api-docs.retroachievements.org/)). Every endpoint is a `GET` to `https://retroachievements.org/API/<Endpoint>.php` and returns JSON. The web API key goes in the `y` query parameter.

```bash
curl "https://retroachievements.org/API/API_GetUserProfile.php?u=MaxMilyin&y=$RA_WEB_API_KEY"
```

### Key links

| What | Link |
| --- | --- |
| Web API docs (home) | [api-docs.retroachievements.org](https://api-docs.retroachievements.org/) |
| Getting started (key setup, quick start) | [Getting Started](https://api-docs.retroachievements.org/getting-started.html) |
| Motto verification method | [Standalones Integration Guide](https://api-docs.retroachievements.org/connect/standalone.html) |
| Official JS/TS client (for the Hono API) | [@retroachievements/api on npm](https://npmjs.com/package/@retroachievements/api) · [GitHub](https://github.com/RetroAchievements/api-js) |
| Unofficial Dart client (reference only) | [retroachievements on pub.dev](https://pub.dev/packages/retroachievements) |
| RAWeb source (how each endpoint is built) | [RetroAchievements/RAWeb](https://github.com/RetroAchievements/RAWeb) |
| Requesting new API data | GitHub Discussion thread, linked from the docs home page |

### Keys and auth

- **Web API key:** found in the RA control panel under "Keys". It's a 32-character, case-sensitive key, and RA says to treat it like a password.
- **One production key, never more.** Production uses a single key on a dedicated "savesfm" service account, which RA staff are told about during outreach. Spreading load across several keys or alt accounts to get past the rate limit is off the table: it goes against how RA expects the API to be used, and it could get every key blocked.
- **Environment keys:** local development and staging both use Matthew's personal key. That's two keys in total, both on real accounts, and neither is ever used to add capacity. Staging only polls a handful of test users, so the personal key covers it.
- **Needing more capacity:** ask RA for a higher limit, and don't add keys.
- **Storage:** store each key as a Worker secret (`wrangler secret put RA_WEB_API_KEY`). Keys never go into the React or Flutter clients. Every RA call goes through the Hono API, so the Dart client is only useful as a reference.
- **JS client setup:** `buildAuthorization({ username, webApiKey })`, then pass that object to every function.
- **Connect API:** not needed. That's RA's private API for emulators, with its own token.

### Usage rules

- Rate limiting is enabled, and RA doesn't publish the exact limit. They expect apps to be reasonable, cache, and preload where possible, and they'll talk through specific use cases.
- Keeping up with API changes is the app's responsibility. Follow the RA Discord and RAWeb releases.
- The game list endpoint's responses can be huge. RA says to cache it aggressively, and frequent calls may get your bandwidth looked at.
- The user summary endpoint is slow and over-fetches. RA recommends the profile endpoint for basic info.
- Any `u` parameter takes a username or a ULID. Store the ULID, so links survive RA username changes.

### Endpoints saves.fm uses

| Used for | Endpoint | Params | Notes |
| --- | --- | --- | --- |
| Motto check, now playing | [API\_GetUserProfile](https://api-docs.retroachievements.org/v1/get-user-profile.html) | `u` | Returns Motto, RichPresenceMsg, LastGameID, ID, TotalPoints. Cheap: use this for verification and regular presence polling. |
| Presence freshness (occasional) | [API\_GetUserSummary](https://api-docs.retroachievements.org/v1/get-user-summary.html) | `u`, `g` (recent games count), `a` (recent achievements count) | Slow. Adds RichPresenceMsgDate, Status and RecentlyPlayed. Call sparingly. |
| Backfill: games with progress | [API\_GetUserCompletionProgress](https://api-docs.retroachievements.org/v1/get-user-completion-progress.html) | `u`, `c` (count), `o` (offset) | Paginated, up to 500 per page. Includes the highest award per game (beaten, mastered). |
| Backfill: unlock history | [API\_GetAchievementsEarnedBetween](https://api-docs.retroachievements.org/v1/get-achievements-earned-between.html) | `u`, `f`, `t` (epoch seconds) | Returns each unlock with date, hardcore flag, achievement ID, game and badge. |
| Per-game detail | [API\_GetGameInfoAndUserProgress](https://api-docs.retroachievements.org/v1/get-game-info-and-user-progress.html) | `u`, `g`, `a=1` (include awards) | Game metadata plus one user's progress on it. Good for game pages and fixing gaps. |
| Polling new unlocks | [API\_GetUserRecentAchievements](https://api-docs.retroachievements.org/v1/get-user-recent-achievements.html) | `u`, `m` (minutes back, default 60) | Set `m` to the minutes since the last poll plus a buffer. Dedupe on (user, achievement). |
| Recently played | [API\_GetUserRecentlyPlayedGames](https://api-docs.retroachievements.org/v1/get-user-recently-played-games.html) | `u`, `c`, `o` | Helps estimate sessions for games with few unlocks. |
| Game metadata cache | [API\_GetGameExtended](https://api-docs.retroachievements.org/v1/get-game-extended.html) | `i`, `f=5` (include unofficial) | Achievements, unlock counts, player counts. Refresh only when a set changes. |
| Console list | [API\_GetConsoleIDs](https://api-docs.retroachievements.org/v1/get-console-ids.html) | `a=1` (active), `g=1` (game systems only) | Fetch once and cache. |
| Catalog for the Finder | [API\_GetGameList](https://api-docs.retroachievements.org/v1/get-game-list.html) | `i` (console), `f=1` (has achievements), `h` (hashes), `c`, `o` | Very large responses. Cache aggressively and refresh rarely. |
| Achievement of the Week | API\_GetAchievementOfTheWeek | none beyond the key | Current AotW only; poll once a day and store each new one in aotw\_history |
| Want to Play sync | Want to Play Games List (getUserWantToPlayList in the JS client) | u, plus paging | Check the docs for the exact endpoint name and any access rules (e.g. whether the target user must follow the caller) before building |

### Backfill recipe

1. Call `API_GetUserProfile` to get the ID and MemberSince, and to confirm the motto code.
2. Page through `API_GetUserCompletionProgress` with `c=500` to get every game with progress.
3. Walk `API_GetAchievementsEarnedBetween` in 30-day windows from MemberSince to now, and upsert into `unlocks`: a softcore entry sets `unlocked_at`, a hardcore entry sets `hardcore_unlocked_at` (and `unlocked_at` if it's the first). Fall back to `API_GetGameInfoAndUserProgress` for any game whose unlock count doesn't match; its per-achievement DateEarned and DateEarnedHardcore fill both columns.
4. Call `API_GetGameExtended` for any game not in the cache.
5. Mark the backfill done, and switch the user to tiered polling with `API_GetUserRecentAchievements`.

Some newer docs pages show `u` as "username or ULID". Confirm in the docs which endpoints accept a ULID before relying on it everywhere.

## Policies and operations

### Privacy and data rights

- **Privacy policy:** a plain-language page covering what's stored (email, passkeys, RA username and ID, unlock history, sessions, presence), why it's stored, how long it's kept, and that nothing is sold or used for ads. No third-party ad trackers. The policy lists every third-party processor: Cloudflare (hosting, email), Sentry (error reports), Firebase Cloud Messaging (push, opt-in) and Ko-fi (supporter payments).
- **Delete account:** self-serve and immediate. It removes every row tied to the user (unlocks, sessions, presence, follows, passkeys, email, supporter status). Backups age out on their normal schedule, and the policy says how long that takes.
- **Export:** a full history download as JSON and CSV (unlocks, sessions, profile, stats). It's built in a background job, stored in R2, and the link is emailed and expires after 24 hours.
- **Pause tracking:** stops polling without deleting anything. On resume, the gap is backfilled with `API_GetAchievementsEarnedBetween`.

### Terms of Service

A short, plain-language page next to the privacy policy, covering:

- **Acceptable use:** no scraping through saves.fm, no automated or fake accounts, no abusing other users, and no attempts to get around rate limits.
- **Not affiliated with RetroAchievements:** saves.fm is an independent fan project. Achievement and game data belongs to RA and its users.
- **License and warranty:** the code is AGPL-3.0, the service is provided as-is with no warranty, and features may change or the service may shut down.
- **Supporter terms:** perks are cosmetic, payments and refunds are handled through Ko-fi, and core features are never paid.

### Untracked RA accounts

- The `Untracked` flag from `API_GetUserProfile` is checked at link time and again on a regular schedule, and stored on `ra_links`.
- An account can be Untracked because RA staff flagged it, or because the player asked to stay off RA's global leaderboard. saves.fm treats both cases the same way, and never labels anyone as flagged. Untracked users can sign up and see their own stats. They never appear in global charts, game pages, Player 2, recommendations or other users' feeds.

### Accessibility (WCAG 2.2 AA, web and Flutter)

- **Contrast:** the token build checks contrast and fails below 4.5:1 for text and 3:1 for UI components and chart marks.
- **Charts:** every chart has a short text summary and a data-table view.
- **Web:** full keyboard support, visible focus, semantic HTML and ARIA where needed, and screen reader testing with VoiceOver and NVDA.
- **Flutter:** Semantics labels on custom widgets, and testing with VoiceOver and TalkBack.
- **Text and motion:** text scales to 200% without breaking layouts. Reduced-motion settings turn off animations and CRT/scanline effects.
- **Fonts:** the pixel display font is only for short display text, never body copy, and it always has accessible labels.

### Moderation

- Display names are always the RA username, and tags come from RA genres plus a curated list. There's no free-text user content at launch.
- A contact email handles reports for now. A real reporting flow gets added if comments or custom text ever ship.

### Supporters (Ko-fi)

- A Ko-fi webhook posts to a Hono endpoint. The endpoint checks Ko-fi's verification token and matches the payer's email to a verified saves.fm email.
- Unmatched payments go to a claim queue, and the supporter claims the perk from their settings page.
- Perks are cosmetic only (profile themes, a supporter badge). Core features are never paid. Perks are sold on the web only. The iOS and Android apps have no donation links, Ko-fi mentions or perk store, because App Store and Google Play payment rules generally require in-app purchase for tips or digital perks. Perks bought on the web may still show in the apps; confirm that passes review before the first submission.

### Email (Cloudflare Email Service)

- Sends through the Workers `send_email` binding, so there's no API key to store. Email Sending is in public beta and needs the Workers Paid plan.
- Sent from `notices@saves.fm`, with SPF, DKIM and DMARC set up on the domain before launch.
- All sending goes through one small mail module, so switching providers (e.g. to Resend) is a one-file change if the beta causes problems. The opt-in weekly digest is the only non-essential email. It has its own setting, separate from account notices, and every digest includes a one-click unsubscribe link and a List-Unsubscribe header.

### Monitoring and backups

- **Workers Observability** covers API logs and metrics, and **Sentry** covers crash and error reporting in React and Flutter.
- **Health dashboards:** poll success rate, RA error and 429 counts, queue backlog, backfill duration, and email send failures. Alerts fire when any of these spike.
- **Backups:** D1 Time Travel for point-in-time restore, plus a scheduled export to R2.

### Brand direction

- A clean, modern layout with Last.fm-style clarity, mixed with real retro elements.
- **Retro elements:** a pixel display font for the logo, headings and big stat numbers; a console-era accent palette; and CRT/scanline textures in decorative places like Rewind cards, the landing hero and empty states.
- **Readability:** body text uses a clean, readable sans so long pages stay comfortable.
- **Originality:** all artwork is original. No console makers' logos, and no imitations of real cartridge labels.

### RetroAchievements outreach

- Once there's a working prototype, before the public launch, share it with RA staff through their Discord or the API discussion thread.
- Cover the use case, the polling plan and tiers, the expected request volume, and a contact. Adjust the plan based on their feedback.

## Roadmap, risks and open questions

### Roadmap

Every feature ships on web first. The mobile apps come last, at full parity.

1. **Foundation:**
   - Monorepo, design tokens with light and dark themes, translation-ready strings, and the OpenAPI pipeline with public-ready `/v1` endpoints.
   - Passkey and email registration, RA motto verification, and the share-image service.
   - Local, staging and production environments.
2. **MVP on web:** backfill, change-triggered polling, profile, charts and history. Matthew's account is backfilled first, to tune session estimates.
3. **Prototype demo to RA staff:** share the request budget and polling plan, then adjust from their feedback.
4. **Launch checks:** all three launch criteria below are met.
5. **Public web launch,** with the changelog and status page. There's no closed beta.
6. **Last.fm-style pages:** game pages, global charts, now playing, tags.
7. **Player 2:** follows, compatibility, friends feed.
8. **Discovery:** recommendations and the finder.
9. **Rewind:** year-end recap and share cards, ready by early December. The first one is December 2027.
10. **Profile cards, yearly goals and supporters.**
11. **Notifications on web:** in-app feed and weekly digest.
12. **Lists and percentiles.**
13. **Public API and Discord bot.**
14. **iOS and Android:** both apps ship together with every feature, plus push and home-screen widgets.

### Launch criteria

There's no beta, so the public launch waits until all three of these are true:

- [ ] **Backfill works on varied accounts:** tested on Matthew's account and on several public RA profiles of different sizes, read-only with no sign-up, including at least one very large library.
- [ ] **Load test passes:** 5,000 simulated users polling against recorded RA responses stay under the daily call cap and the requests-per-second limit, with no queue backlog.
- [ ] **Accessibility audit passes:** WCAG 2.2 AA checks on web. VoiceOver and TalkBack passes are part of the mobile release in v2.0.0.

### Risks

- **RA rate limits or API changes:** caching, a central rate limiter, tiered polling, early contact with RA staff, and following their Discord and release notes.
- **Session estimates feel wrong:** label them as estimates, make the gap threshold tunable, and tune it on real history before launch.
- **D1 growth:** watch database size and plan sharding early.
- **Profiles changing to private, or RA renames:** handle missing data gracefully and re-verify when needed.
- **Trademark:** stay clearly unaffiliated. Use no RA logos beyond what their guidelines allow, and borrow Last.fm's ideas without copying its branding.

### Decisions

| Topic | Decision |
| --- | --- |
| Profile visibility | Public by default, with a private toggle |
| Softcore vs hardcore | Counted together by default, with a hardcore-only filter on every chart |
| Open source | The whole stack is open from day one (web, Flutter, API, token pipeline); secrets stay in Worker config |
| Sign-in | Passkeys, with a verified email collected at registration |
| Account recovery | RA motto re-verification or a verified-email recovery link, then register a new passkey |
| Funding | Free, with optional donations (e.g. Ko-fi, GitHub Sponsors) plus optional cosmetic supporter perks (profile themes, badges); core features never go behind a paywall |
| Name and domains | saves.fm, plus a savesfm.com redirect (saves-fm.com also free). Renamed from cartridge.fm on Nov 7, 2026: cartridge.gg is Cartridge Gaming Company, an iPhone game studio, so the name clashed in our own category. saves.com is taken. On Nov 7, 2026, saves.fm, savesfm.com, saves-fm.com, GitHub `saves-fm` (now claimed), npm `@savesfm`, Bluesky and the Discord vanity were free, and USPTO had no SAVES mark for this kind of software |
| Social handles | X @SaveSFM is taken (an unrelated community account), so X uses an alternative such as @savesdotfm or @saves_fm. Bluesky uses @saves.fm (domain handle). Instagram/Threads @savesfm to be checked by hand |
| Untracked RA accounts | Can sign up and see their own stats; left out of all global and social features |
| License | AGPL-3.0 |
| Accessibility | WCAG 2.2 AA on web and Flutter |
| Data rights | Self-serve delete, full export (JSON/CSV), pause tracking, plain-language privacy policy |
| Tags | RA genres plus a curated tag list; no free text |
| Display names | Always the RA username |
| Supporter payments | Ko-fi, with its webhook granting perks |
| Email provider | Cloudflare Email Service (public beta, Workers Paid plan) |
| Monitoring | Workers Observability plus Sentry in React and Flutter |
| Brand direction | Clean modern UI with full retro accents (pixel display type, console-era palette, CRT textures in decorative spots) |
| RA outreach | After a working prototype, before the public launch. Not a formal launch requirement, but strongly recommended since there's no beta |
| Scale target | Designed for up to \~5,000 users in year one; \~107k RA calls/day estimated, 120k/day cap to confirm with RA |
| Polling | Profile check each cycle; unlocks fetched only when a points total changes, plus a periodic fallback |
| Rate limiter | One Durable Object enforcing requests per second and the daily cap; not KV |
| Now playing freshness | RichPresenceMsg changing between checks means live; User Summary only as an occasional tiebreaker |
| Hardcore upgrades | unlocks keeps both unlocked\_at and hardcore\_unlocked\_at; the hardcore filter uses the hardcore date |
| Global chart updates | Recomputed on a 15–60 minute cron, not after each poll |
| Mobile pipeline before v2.0.0 | A minimal Flutter build with the generated theme and client, plus one golden test, runs in CI from v0.2.0 |
| First Rewind | December 2027 |
| API keys | One production key on a dedicated service account; personal key for local and staging; never extra keys for capacity |
| Time zones | Auto-detected and editable; stored in UTC; weeks start Monday |
| Platforms | Every feature ships on web first; iOS and Android ship together last, at full parity |
| Perks in mobile apps | Sold on the web only; no donation links or perk store in the apps |
| Environments | Local, staging (with PR previews) and production |
| Repo | Monorepo with pnpm workspaces and Melos, at `saves-fm/saves` |
| Milestones | One per version: v0.1.0 setup, v0.2.0 foundation, v0.3.0 data pipeline, v0.4.0 MVP web, v0.5.0 launch readiness, v1.0.0 public web launch, v1.1.0–v1.8.0 feature releases, v2.0.0 mobile apps |
| Branching | Push straight to `main` with CI on every push; `release/vX.Y.Z` branches are cut at each tag by `release.yml`; contributor PRs get CI and preview deploys |
| Session estimates | Start at a 45-minute gap; tuned on Matthew's own history before launch |
| Beta | No beta; public launch gated on the three launch criteria |
| Terms of Service | Acceptable use, not affiliated with RA, AGPL and no warranty, supporter terms |
| Languages | English at launch, translation-ready from day one |
| Themes | Light and dark at launch; more themes later as supporter perks |
| Share images | Satori + resvg in a Worker, cached in R2 |
| Public API | Designed public-ready now; opened after launch with keys and rate limits |
| Profile cards | SVG, PNG and HTML embed, with several layouts |
| Widgets | Now playing, Streak, This week's top 3 |
| Notifications | In-app feed always on; push and weekly digest opt-in |
| Yearly goals | Masteries/beaten, points/unlocks, consoles, custom game lists |
| Lists | Catalog games with template titles; no free text |
| Percentiles | Among public, tracked users only; users can hide their own |
| Discord bot | Opt-in, after Player 2 ships |
| Changelog and status | Changelog from GitHub releases; status page from the health metrics |
| Activity heatmap | Profile, profile cards and Rewind; respects the hardcore filter |
| Want to Play | Read-only sync of the user's RA list; feeds the Finder |
| Spoiler protection | Account setting plus reveal one at a time |
| Achievement of the Week | Home card, notification, history recorded from launch |
| Retro Ratio | Profile, per game, charts and Rewind; users can hide it |
| Unlock alerts | Friends' masteries only; no alerts for your own unlocks |
| Rewind extras | Days active and streak, rarest unlock, vs. average member, year over year |
| Watch apps | Apple Watch (SwiftUI) and Wear OS (Kotlin/Compose) in v2.0.0: complication plus a glance app or tile |
| Home Assistant | Official example and docs with the public API |

## Setup before writing code

Everything here happens before the first commit, or before the milestone it's tagged with. Most of it is accounts, keys and assets that code depends on.

### Before v0.1.0 (needed to start)

- [ ] **Domains:** register saves.fm and savesfm.com (and optionally saves-fm.com) with a registrar that supports .fm, then point DNS at Cloudflare. Check .fm renewal pricing first.
- [ ] **Handles:** claim the GitHub org `saves-fm` (done Nov 7, 2026), the npm `@savesfm` scope, Bluesky @saves.fm, an X handle (not @SaveSFM, which is taken), and Instagram/Threads @savesfm if free.
- [ ] **Cloudflare:** create an account and upgrade to the Workers Paid plan, which Email Sending requires. Turn on 2FA.
- [ ] **GitHub:** create the `saves-fm` org and the `saves-fm/saves` repo. Work is pushed straight to `main`, with CI on every push; contributor PRs get CI and preview deploys. Turn on Dependabot and secret scanning.
- [ ] **RetroAchievements keys:**
  - Create the dedicated `savesfm` service account.
  - Copy its web API key for production.
  - Copy your personal key for local development and staging.
  - Store both in a password manager.
- [ ] **Sentry:** create an account and two projects, one for web and one for Flutter.
- [ ] **Local tooling:**
  - JavaScript: Node LTS, pnpm, Wrangler and the `gh` CLI.
  - Flutter: the stable SDK and Melos.
  - Mobile builds: Xcode (iOS) and Android Studio (Android).
- [ ] **GitHub backlog:** create the labels and milestones from the section below, then generate the issues.
- [ ] **Project board:** a GitHub Projects board with columns Backlog, Ready, In progress, Review and Done.

### Before v0.2.0 (Foundation)

- [ ] **Brand basics:** the logo direction, palette for light and dark themes, a readable body sans font and a pixel display font. Check every font's license (e.g. SIL OFL) for web, app and image use, since the share-image Worker bundles them.
- [ ] **Starting tokens:** first-pass values for type scale, spacing, radius and motion.
- [ ] **Email sending domain:** add saves.fm to Cloudflare Email Service, publish SPF, DKIM and DMARC records, and confirm a test email reaches inboxes.
- [ ] **String catalog format:** pick the shared source format and the tool that generates ICU messages for web and ARB files for Flutter.

### Before v0.3.0 (Data pipeline)

- [ ] **Session ground truth:** write down 10–20 real play sessions from your own history (game, rough start and end, date) to tune the session gap against.
- [ ] **Test profiles:** list public RA profiles of different sizes (small, medium, and at least one very large library) for backfill fixtures and launch testing.
- [ ] **Fixtures:** record RA responses for every endpoint used, from those profiles, into the repo's fixtures folder.

### Before v0.4.0 (MVP web)

- [ ] **Legal drafts:** first drafts of the privacy policy and Terms of Service. Have someone review them before launch if possible.
- [ ] **Contact address:** set up a support or report email address, e.g. hello@saves.fm, using Cloudflare Email Routing.

### Before v2.0.0 (Mobile apps)

- [ ] **Apple Developer Program:** $99/yr. Enrolling as an organization needs a D-U-N-S number, which can take weeks, so start early.
- [ ] **Google Play Console:** one-time $25 fee, plus identity verification.
- [ ] **App identifiers:** bundle IDs (e.g. `fm.saves.app`) and signing keys, stored safely.
- [ ] **App Store and Play listing basics:** privacy labels, screenshots and support URL.

### Before v1.5.0 (Ko-fi) and v2.0.0 (Firebase)

- [ ] **Ko-fi:** create the account, turn on webhooks and save the verification token as a Worker secret.
- [ ] **Firebase:** create a project for Cloud Messaging, link the Apple push key (APNs) and add the Android app.

## GitHub milestones and issues

Each `###` heading below is a GitHub milestone named for the version it ships (v0.1.0 to v2.0.0), and each checkbox is one issue, sized at roughly one to three days of work. Issue titles start with their area label. The milestones follow the roadmap order. Every issue is assigned to Matthew, carries its labels, and is written so a contributor could pick it up. Work beyond v2.0.0 goes in issues with no milestone.

Each release tag (`vX.Y.Z`) runs `release.yml`, which pushes a `release/vX.Y.Z` branch at the tag and closes the milestone with links to the release, tag, branch and the commits since the previous version.

### Labels

- **Area:** `area:api`, `area:data`, `area:web`, `area:mobile`, `area:tokens`, `area:infra`, `area:a11y`, `area:i18n`, `area:docs`
- **Type:** `type:feature`, `type:chore`, `type:test`, `type:docs`, `type:bug`
- **Priority:** `p0` (blocks launch), `p1` (should ship), `p2` (nice to have)
- **Platform** (for parity tracking): `platform:web`, `platform:ios`, `platform:android`

### v0.1.0: Project setup

- [ ] &#91;infra\] Create monorepo: `apps/web`, `apps/mobile`, `apps/api`, `packages/tokens`, `packages/api-schema`; pnpm workspaces + Melos
- [ ] &#91;infra\] Add AGPL-3.0 license, README, CONTRIBUTING, code of conduct, issue and PR templates (with a parity checklist)
- [ ] &#91;infra\] CI: lint, typecheck, unit tests for TS and Dart on every push and PR, with the CI badge added to the README
- [ ] &#91;infra\] Cloudflare setup: staging and production Workers, D1, R2, KV and Queues, plus Wrangler config per environment
- [ ] &#91;infra\] PR preview deploys to staging
- [ ] &#91;infra\] `release.yml`: on a version tag, push `release/vX.Y.Z` and close the milestone with release, tag, branch and compare links; regenerate the committed `docs/badges/release.svg` on each version bump, with a test that checks it, and swap the status badge for it
- [ ] &#91;infra\] Secrets: RA web API keys as Worker secrets (personal key for local and staging, service-account key for production)
- [ ] &#91;infra\] Sentry projects for web and Flutter; turn on Workers Observability
- [ ] &#91;infra\] Domains: saves.fm DNS on Cloudflare, plus a .com redirect

### v0.2.0: Foundation

- [ ] &#91;tokens\] Token source for colors, type, spacing, radius and motion, with light and dark themes
- [ ] &#91;tokens\] Build step to generate CSS variables and a Dart theme file
- [ ] &#91;tokens\] Contrast check in the token build (fail below 4.5:1 for text and 3:1 for UI)
- [ ] &#91;i18n\] Shared string catalog generating ICU messages for web and ARB files for Flutter, with locale-aware dates and numbers
- [ ] &#91;api\] Hono app skeleton: `/v1` routing, Zod schemas, OpenAPI generation
- [ ] &#91;api\] Generate the TypeScript and Dart API clients from OpenAPI in CI
- [ ] &#91;mobile\] Minimal Flutter CI app: uses the generated Dart theme and client, one golden test, fails the PR on Dart breakage
- [ ] &#91;data\] D1 migrations for core tables (users, passkeys, ra\_links, verification\_codes, games, achievements, unlocks, sessions)
- [ ] &#91;api\] Email registration with a one-time code (Cloudflare Email Service binding, mail module)
- [ ] &#91;api\] Passkey registration and sign-in (WebAuthn), with multiple passkeys per user
- [ ] &#91;api\] RA motto verification flow (code generation, expiry, profile check, linking)
- [ ] &#91;api\] Account recovery via RA motto or email link, with security alert emails and rate limits
- [ ] &#91;infra\] Email domain setup: SPF, DKIM and DMARC for notices@saves.fm
- [ ] &#91;api\] Share-image Worker: Satori + resvg WASM, bundled fonts, R2 cache keyed by content
- [ ] &#91;api\] RA client wrapper around `@retroachievements/api`, with the shared Durable Object rate limiter (requests-per-second plus daily cap)
- [ ] &#91;test\] Record RA response fixtures for every endpoint used

### v0.3.0: Data pipeline

- [ ] &#91;data\] Backfill job: profile, then completion progress (paged), then earned-between in 30-day windows, then game metadata, through Queues
- [ ] &#91;data\] Backfill progress reporting ("Importing 214 of 640 games")
- [ ] &#91;data\] Game and achievement metadata cache, with refresh when a set changes
- [ ] &#91;data\] Change-triggered polling: profile check per tier, unlock fetch when a points total changes, periodic fallback
- [ ] &#91;data\] Polling tiers and automatic tier changes based on activity
- [ ] &#91;data\] Cap-aware scheduling: stretch idle, then weekly intervals near the daily cap; backfills in a low-priority queue
- [ ] &#91;data\] Session estimation (gap-based, padded), tuned on Matthew's history
- [ ] &#91;data\] Time zone handling: store UTC, compute days and weeks (ISO, Monday) in the user's time zone
- [ ] &#91;data\] Stat rollups (weekly, monthly, yearly, all time; all and hardcore-only)
- [ ] &#91;data\] Untracked flag check at link time and on a schedule
- [ ] &#91;test\] Unit tests for sessions, rollups and time zone edge cases (DST, midnight crossings)
- [ ] &#91;data\] Softcore-to-hardcore upgrades: upsert hardcore\_unlocked\_at in backfill and polling, with tests for the hardcore filter
- [ ] &#91;data\] Daily Achievement of the Week poll, storing each new AotW in aotw\_history from launch day
- [ ] &#91;data\] Want to Play sync (read-only mirror, refreshed with polling)
- [ ] &#91;data\] Retro Ratio from cached true points, per game and overall

### v0.4.0: MVP web

- [ ] &#91;web\] App shell: routing, theming (system, light, dark), i18n wiring, generated API client
- [ ] &#91;web\] Registration and sign-in UI (email code, passkey)
- [ ] &#91;web\] RA linking UI with motto instructions and verification states
- [ ] &#91;web\] Public profile page with server-rendered link-preview images
- [ ] &#91;web\] Charts: top games, consoles and genres by period, with a hardcore filter, text summaries and table views
- [ ] &#91;web\] History timeline with estimated sessions and "on this day"
- [ ] &#91;web\] Settings: time zone, privacy (public/private), pause tracking, theme, email
- [ ] &#91;web\] Data rights: export (JSON/CSV to R2, emailed link) and self-serve account deletion
- [ ] &#91;docs\] Privacy policy and Terms of Service pages
- [ ] &#91;a11y\] Keyboard, focus and screen reader pass on all MVP screens
- [ ] &#91;web\] Activity heatmap on profiles (user time zone, hardcore filter, accessible text alternative)
- [ ] &#91;web\] Spoiler protection setting, with click-to-reveal for each locked achievement
- [ ] &#91;web\] Retro Ratio profile stat with an explanation and a hide toggle
- [ ] &#91;web\] Want to Play list on profiles (read-only, linking to RA for edits)

### v0.5.0: Launch readiness

- [ ] &#91;test\] Backfill tests on varied public RA profiles, including a very large library
- [ ] &#91;test\] Load test: 5,000 simulated users against fixtures, staying under the cap and the rate limit
- [ ] &#91;a11y\] WCAG 2.2 AA audit on web, fixing every finding
- [ ] &#91;infra\] Health dashboards and alerts: poll success, RA errors and 429s, queue backlog, backfill time, email failures
- [ ] &#91;infra\] D1 Time Travel, plus a scheduled export to R2, with a tested restore
- [ ] &#91;web\] Status page fed by the health metrics
- [ ] &#91;web\] Changelog page generated from GitHub releases
- [ ] &#91;docs\] RA staff demo: write-up of the request budget and polling plan, shared, feedback logged

### v1.0.0: Public web launch

- [ ] &#91;infra\] Production cutover checklist and rollback plan
- [ ] &#91;docs\] Launch post for the RA community
- [ ] &#91;infra\] Post-launch watch: first-week metrics review and request-budget check against the estimate

### v1.1.0: Last.fm-style pages

- [ ] &#91;api\] Game page endpoint: players, unlocks this week, top players, your history
- [ ] &#91;web\] Game pages
- [ ] &#91;data\] Global weekly charts (UTC weeks, public tracked users only), with risers and fallers, recomputed on a 15–60 minute cron
- [ ] &#91;web\] Global charts pages
- [ ] &#91;data\] Now playing from presence (profile polling; live when RichPresenceMsg changed between checks, summary only as a tiebreaker)
- [ ] &#91;web\] Now playing on profiles and the friends feed
- [ ] &#91;data\] Tags: RA genres plus a curated tag list
- [ ] &#91;web\] Tag browsing
- [ ] &#91;web\] Achievement of the Week home page card, with your progress on that game
- [ ] &#91;web\] Per-game Retro Ratio on game pages

### v1.2.0: Player 2

- [ ] &#91;api\] Follows, plus follow and unfollow endpoints
- [ ] &#91;data\] Compatibility score from overlapping games, consoles and masteries
- [ ] &#91;web\] Compare page: score, shared favorites, only-one-of-you games
- [ ] &#91;web\] Friends feed (masteries, now playing)

### v1.3.0: Discovery

- [ ] &#91;data\] Recommendations based on overlap between users
- [ ] &#91;data\] Difficulty estimate from unlock rarity
- [ ] &#91;api\] Finder endpoint: console, genre, length, difficulty, started but unfinished
- [ ] &#91;web\] Recommendations and Finder pages
- [ ] &#91;data\] Use Want to Play and Retro Ratio in Finder ranking and the difficulty filter

### v1.4.0: Rewind

- [ ] &#91;data\] Year-end rollup: hardest unlocks, top consoles, busiest months, streaks, top game pages, Player 2 match
- [ ] &#91;api\] Rewind share cards via the share-image service
- [ ] &#91;web\] Rewind experience (respecting reduced motion)
- [ ] &#91;infra\] Rewind generation job and load check for December
- [ ] &#91;data\] Rewind extras: days active, longest streak, rarest unlock with % of players, vs. the average member, year over year, toughest-year Retro Ratio
- [ ] &#91;web\] Rewind heatmap card

### v1.5.0: Profile cards, goals and supporters

- [ ] &#91;api\] Profile card endpoints: SVG and PNG, with recently played, top consoles, streak and latest mastery layouts
- [ ] &#91;web\] HTML embed and a card builder page
- [ ] &#91;data\] Yearly goals: masteries/beaten, points/unlocks, consoles, custom lists, with progress tracking
- [ ] &#91;web\] Goals UI and profile progress, plus a Rewind tie-in
- [ ] &#91;api\] Ko-fi webhook: token check, email matching, claim queue
- [ ] &#91;web\] Supporter page and perk claiming (web only, permanently)
- [ ] &#91;api\] Heatmap profile card layout (SVG and PNG)

### v1.6.0: Notifications (web)

- [ ] &#91;api\] Notification generation: milestones, throwbacks, near-mastery, friends' masteries, goal progress
- [ ] &#91;web\] In-app notifications feed and per-type preferences
- [ ] &#91;api\] Weekly email digest (opt-in, one-click unsubscribe, List-Unsubscribe header)
- [ ] &#91;api\] Push-ready notification model, so mobile push in v2.0.0 only adds a delivery channel
- [ ] &#91;api\] Friends' mastery and beaten alerts
- [ ] &#91;api\] New Achievement of the Week notification
- [ ] &#91;web\] AotW history on profiles

### v1.7.0: Lists and percentiles

- [ ] &#91;api\] Lists with template titles and ordered games
- [ ] &#91;web\] List builder and list pages
- [ ] &#91;data\] Percentiles among public tracked users, with a hide option
- [ ] &#91;web\] Percentile display on profiles

### v1.8.0: Public API and Discord bot

- [ ] &#91;api\] API keys (hashed), per-key rate limits, developer key management page
- [ ] &#91;docs\] Public API docs site generated from OpenAPI
- [ ] &#91;api\] Open public `/v1` endpoints for public tracked profiles
- [ ] &#91;api\] Discord bot: opt-in server linking, posts for friends' masteries and Rewind highlights
- [ ] &#91;docs\] Home Assistant guide: REST sensor config, plus an example integration in the repo

### v2.0.0: Mobile apps (iOS + Android, full parity)

Every web feature exists by this point. The apps ship together, matching web screen for screen, plus the mobile-only features.

- [ ] &#91;mobile\] Flutter app shell: theming from the generated Dart tokens, ARB i18n, generated Dart client
- [ ] &#91;mobile\] Passkey sign-in and email registration on iOS and Android
- [ ] &#91;mobile\] RA linking flow
- [ ] &#91;mobile\] Profile, charts and history screens
- [ ] &#91;mobile\] Game pages, global charts, now playing and tags
- [ ] &#91;mobile\] Player 2: compare page and friends feed
- [ ] &#91;mobile\] Recommendations and Finder
- [ ] &#91;mobile\] Rewind
- [ ] &#91;mobile\] Goals, profile cards (share sheet) and supporter badge display; no donation links or perk store
- [ ] &#91;mobile\] In-app notifications feed and preferences
- [ ] &#91;mobile\] Lists and percentiles
- [ ] &#91;mobile\] Settings, data export and in-app account deletion (App Store requirement)
- [ ] &#91;mobile\] Push via Firebase Cloud Messaging (opt-in), with token lifecycle handling
- [ ] &#91;mobile\] iOS WidgetKit widgets: Now playing, Streak, This week's top 3
- [ ] &#91;mobile\] Android widgets: Now playing, Streak, This week's top 3
- [ ] &#91;docs\] Update the privacy policy for push (Firebase)
- [ ] &#91;a11y\] VoiceOver and TalkBack passes on every screen
- [ ] &#91;test\] Golden screenshot tests for key screens, compared against web for parity
- [ ] &#91;infra\] Store listings, privacy labels, TestFlight and Play internal testing, then release
- [ ] &#91;mobile\] Heatmap, spoiler protection, Retro Ratio, Want to Play and AotW screens
- [ ] &#91;mobile\] Apple Watch app (SwiftUI): now playing/streak complication and a recent-unlocks app
- [ ] &#91;mobile\] Wear OS app (Kotlin/Compose): tile and complication, matching Apple Watch

To create these in GitHub, each milestone heading becomes a milestone and each checkbox becomes an issue. A short script using `gh` (`gh api` for milestones, `gh issue create --milestone --label` for issues) can turn this section into the full backlog in one pass.
