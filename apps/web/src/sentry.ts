import * as Sentry from '@sentry/react';

// Error reporting for the web app (Sentry project saves-web). Errors only:
// no session replay, no tracing, and no personal data (IP addresses, cookies)
// attached, in line with the privacy policy. Off in local dev.
export function environmentFor(hostname: string): string {
  if (hostname.startsWith('pr-')) return 'preview';
  if (hostname.includes('-staging.')) return 'staging';
  return 'production';
}

export function initSentry() {
  const dsn = import.meta.env.VITE_SENTRY_DSN;
  if (!dsn || import.meta.env.DEV) return;
  Sentry.init({
    dsn,
    environment: environmentFor(location.hostname),
    // Sentry v11 collects user info, cookies, headers, bodies and query params by default
    dataCollection: { userInfo: false, cookies: false, httpHeaders: false, httpBodies: [], urlQueryParams: false },
    tracesSampleRate: 0,
  });
}
