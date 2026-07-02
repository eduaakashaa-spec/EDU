import { test, expect } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

const BASE = process.env.BASE_URL || 'http://127.0.0.1:5000';
const pages: string[] = JSON.parse(
  fs.readFileSync(path.join(__dirname, 'all_pages.json'), 'utf8')
);

// Noise we don't treat as failures: third-party CDN hiccups, favicons, etc.
const IGNORE = [
  /favicon/i,
  /net::ERR_/,
  /Failed to load resource.*(googleapis|gstatic|jsdelivr|cloudflare|unpkg)/i,
];

for (const p of pages) {
  test(`page ${p} renders without errors`, async ({ page }) => {
    const errors: string[] = [];
    page.on('pageerror', (err) => errors.push(`pageerror: ${err.message}`));
    page.on('console', (msg) => {
      if (msg.type() === 'error') errors.push(`console: ${msg.text()}`);
    });

    const resp = await page.goto(BASE + p, { waitUntil: 'load', timeout: 30000 });
    expect(resp, `no response for ${p}`).toBeTruthy();
    expect(resp!.status(), `status for ${p}`).toBeLessThan(400);

    // Give deferred scripts a moment to run
    await page.waitForTimeout(500);

    const real = errors.filter((e) => !IGNORE.some((rx) => rx.test(e)));
    expect(real, `JS errors on ${p}:\n${real.join('\n')}`).toEqual([]);

    // Every page should have rendered visible content
    const textLen = await page.evaluate(() => document.body.innerText.length);
    expect(textLen, `page ${p} looks empty`).toBeGreaterThan(100);
  });
}
