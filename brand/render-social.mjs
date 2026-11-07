// Render the social images from social/templates with Playwright (Chromium).
// usage: node render-social.mjs [path/to/playwright-core]
import { createRequire } from 'module';
import { fileURLToPath } from 'url';
import path from 'path';
const require = createRequire(import.meta.url);
const { chromium } = require(process.argv[2] || 'playwright-core');
const here = path.dirname(fileURLToPath(import.meta.url));
const jobs = [
  ['og-image.html', 1200, 630, 'og-image-1200x630.png'],
  ['og-image.html', 1280, 640, 'github-social-preview-1280x640.png'],
];
const browser = await chromium.launch();
for (const [tpl, w, h, out] of jobs) {
  const page = await browser.newPage({ viewport: { width: w, height: h } });
  // Load from a real file URL so the page can read the fonts and logo next to it
  await page.goto(`file://${path.join(here, 'social', 'templates', tpl)}?w=${w}&h=${h}`);
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(200);
  await page.screenshot({ path: path.join(here, 'social', out) });
  await page.close();
  console.log('rendered', out);
}
await browser.close();
