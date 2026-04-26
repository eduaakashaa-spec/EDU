import { test, expect } from '@playwright/test';

const BASE = 'http://127.0.0.1:5000';

const pages = [
  { path: '/', titlePart: 'EduAakashaA' },
  { path: '/josaa', titlePart: 'JOSAA' },
  { path: '/iiits', titlePart: 'IIIT' },
  { path: '/annanri', titlePart: 'Anna' },
  { path: '/dasa-seat-matrix', titlePart: 'DASA' },
  { path: '/dasa-admissions-guide', titlePart: 'DASA' },
  { path: '/nirf-ranking', titlePart: 'NIRF' },
  { path: '/tnea2026', titlePart: 'TNEA' },
  { path: '/tneamatrix', titlePart: 'TNEA' },
  { path: '/tneapc', titlePart: 'TNEA' },
  { path: '/tnea-cutoff', titlePart: 'TNEA' },
  { path: '/tnea-simulator', titlePart: 'TNEA' },
  { path: '/professional-exam', titlePart: 'Professional' },
  { path: '/internship-programs', titlePart: 'Internship' },
  { path: '/contact', titlePart: 'Contact' },
  { path: '/mbamca-program', titlePart: 'MBA' },
  { path: '/tancet', titlePart: 'TANCET' },
  { path: '/ea-library', titlePart: 'Library' },
  { path: '/tancet-pulse', titlePart: 'TANCET' },
  { path: '/viteee-for-nri', titlePart: 'VITEEE' },
  { path: '/amrita-aeee', titlePart: 'AMRITA' },
  { path: '/nata', titlePart: 'NATA' },
  { path: '/nid', titlePart: 'NID' },
  { path: '/cat', titlePart: 'CAT' },
  { path: '/josaa-assessment', titlePart: 'JOSAA' },
  { path: '/student-assessment', titlePart: 'Assessment' },
  { path: '/conflict-assessment', titlePart: 'Conflict' },
  { path: '/stream-selection', titlePart: 'Stream' },
  { path: '/stream-selectionea', titlePart: 'Stream Selection' },
  { path: '/josaaea-members', titlePart: 'JOSAA' },
  { path: '/exam-schedule', titlePart: 'Exam Schedule' },
  { path: '/join-our-team', titlePart: 'Join' },
];

const aliasRedirects = [
  { path: '/homepage', target: '/' },
  { path: '/contact-us', target: '/contact' },
  { path: '/tnea', target: '/tnea2026' },
];

for (const pg of pages) {
  test(`${pg.path} loads with correct title`, async ({ page }) => {
    const errors: string[] = [];
    page.on('pageerror', (err) => errors.push(err.message));

    await page.goto(`${BASE}${pg.path}`);
    await expect(page).toHaveTitle(new RegExp(pg.titlePart, 'i'));

    // Header nav exists
    await expect(page.locator('#nav')).toBeVisible();

    // Site footer exists
    await expect(page.locator('.footer')).toBeVisible();

    // No JS errors
    expect(errors).toHaveLength(0);
  });
}

for (const alias of aliasRedirects) {
  test(`${alias.path} redirects to ${alias.target}`, async ({ page }) => {
    const response = await page.goto(`${BASE}${alias.path}`);
    expect(response?.status()).toBeLessThan(400);
    await expect(page).toHaveURL(new RegExp(alias.target + '$'));
  });
}

test('contact form is interactive', async ({ page }) => {
  await page.goto(`${BASE}/contact`);
  const form = page.locator('.contact-form');
  await expect(form).toBeVisible();
});

test('TNEA PC calculator works', async ({ page }) => {
  await page.goto(`${BASE}/tneapc`);
  await page.fill('#pcMaths', '90');
  await page.fill('#pcPhysics', '80');
  await page.fill('#pcChemistry', '70');
  await page.click('#pcCalcBtn');
  const result = page.locator('#pcResult');
  await expect(result).toBeVisible();
  const cutoffText = await page.locator('#pcCutoff').textContent();
  // 90/2 + 80/4 + 70/4 = 45 + 20 + 17.5 = 82.5
  expect(cutoffText).toBe('82.50');
});

test('JEE rank converter works on DASA page', async ({ page }) => {
  await page.goto(`${BASE}/dasa-admissions-guide`);
  await page.fill('#jeeRank', '1000');
  const percField = page.locator('#jeePercentile');
  const percVal = await percField.inputValue();
  expect(parseFloat(percVal)).toBeGreaterThan(99);
});

test('TNEA cutoff tab switching works', async ({ page }) => {
  await page.goto(`${BASE}/tnea-cutoff`);
  await expect(page.locator('#tab-predictor')).toBeVisible();
  await page.click('[data-tab="browse"]');
  await expect(page.locator('#tab-browse')).toBeVisible();
});
