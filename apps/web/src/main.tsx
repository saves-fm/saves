import { ErrorBoundary } from '@sentry/react';
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { App } from './App';
import { initSentry } from './sentry';

initSentry();

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ErrorBoundary fallback={<p>Something went wrong. Reload the page to try again.</p>}>
      <App />
    </ErrorBoundary>
  </StrictMode>,
);
