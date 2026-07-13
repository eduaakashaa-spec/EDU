import { test, expect } from '@playwright/test';
const BASE = process.env.BASE_URL || 'http://127.0.0.1:5057';

test('awwwards homepage — desktop: load-in, rank scrubber, engines, finale', async ({ page }) => {
  const errors: string[] = [];
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push('console: ' + m.text()); });
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto(BASE + '/');

  // hero load-in settles: headline lines visible (yPercent back to 0)
  await page.waitForTimeout(2200);
  await expect(page.locator('.aw-hero h1')).toContainText('Luck is not');
  const lineShift = await page.locator('.aw-hero h1 .ln > span').first()
    .evaluate(e => getComputedStyle(e).transform);
  expect(lineShift === 'none' || /matrix\(1, 0, 0, 1, 0, 0\)/.test(lineShift)).toBeTruthy();
  await page.screenshot({ path: '/tmp/aw_hero.png' });

  // scrub INTO the demo: rank should drop & rows flip
  await page.mouse.wheel(0, 2400); await page.waitForTimeout(1200);
  await page.mouse.wheel(0, 1800); await page.waitForTimeout(1200);
  const midRank = await page.locator('#awRank').textContent();
  expect(midRank).not.toBe('5,50,000');
  await page.screenshot({ path: '/tmp/aw_scrub_mid.png' });

  // scrub to end of demo: all five rows SAFE
  for (let i = 0; i < 6; i++) { await page.mouse.wheel(0, 1600); await page.waitForTimeout(500); }
  const safeCount = await page.locator('#awRows .aw-row.safe').count();
  expect(safeCount).toBe(5);
  await page.screenshot({ path: '/tmp/aw_scrub_end.png' });

  // light chapter: counters reach values
  await page.locator('.aw-stats').scrollIntoViewIfNeeded(); await page.waitForTimeout(1700);
  expect(await page.locator('.aw-stat .cnt').first().textContent()).toBe('12,000');

  // engines: horizontal track translates while pinned
  await page.locator('#awEng').scrollIntoViewIfNeeded(); await page.waitForTimeout(600);
  for (let i = 0; i < 4; i++) { await page.mouse.wheel(0, 1200); await page.waitForTimeout(400); }
  const tx = await page.locator('#awTrack').evaluate(e => getComputedStyle(e).transform);
  expect(tx).not.toBe('none');
  await page.screenshot({ path: '/tmp/aw_engines.png' });

  // finale + quotes
  await page.locator('#awFin').scrollIntoViewIfNeeded(); await page.waitForTimeout(800);
  await expect(page.locator('#awFin h2')).toContainText('Same marks');
  expect(await page.locator('.aw-q.on').count()).toBe(1);
  await page.screenshot({ path: '/tmp/aw_finale.png' });

  expect(errors, errors.join('\n')).toHaveLength(0);
});

test('awwwards homepage — mobile: no overflow, demo autoplays', async ({ page }) => {
  const errors: string[] = [];
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto(BASE + '/');
  await page.waitForTimeout(1500);
  // users must not be able to scroll sideways (root clips internal overflow site-wide)
  await page.evaluate(() => window.scrollBy(80, 0));
  expect(await page.evaluate(() => window.scrollX)).toBe(0);
  await page.locator('#awDemo').scrollIntoViewIfNeeded();
  await page.waitForTimeout(5200);            // autoplay story completes
  expect(await page.locator('#awRows .aw-row.safe').count()).toBe(5);
  await page.screenshot({ path: '/tmp/aw_mobile.png', fullPage: false });
  expect(errors, errors.join('\n')).toHaveLength(0);
});
