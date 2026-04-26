/**
 * Scrape live Hostinger site pages for local reference.
 * Content on the Zyro/Hostinger pages is inside iframes (srcdoc), so we
 * also walk into every child frame, wait for it, and extract its rendered
 * HTML + text + structured details. We save:
 *   reference/live_pages/html/<slug>.html          (outer page)
 *   reference/live_pages/html/<slug>.frame-<i>.html (each iframe)
 *   reference/live_pages/text/<slug>.txt           (combined text, outer + frames)
 *   reference/live_pages/meta/<slug>.json          (structured)
 *   reference/live_pages/screens/<slug>.png        (full page screenshot)
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const BASE = 'https://eduaakashaa.in';

const PATHS = [
  '/',
  '/homepage',
  '/iiits',
  '/annanri',
  '/dasa-seat-matrix',
  '/viteee-for-nri',
  '/dasa-admissions-guide',
  '/nirf-ranking',
  '/amrita-aeee',
  '/tnea2026',
  '/tnea',
  '/tneamatrix',
  '/tneapc',
  '/tnea-cutoff',
  '/josaa',
  '/josaa-assessment',
  '/nata',
  '/nid',
  '/mbamca-program',
  '/tancet-pulse',
  '/cat',
  '/student-assessment',
  '/exam-schedule',
  '/professional-exam',
  '/stream-selection',
  '/stream-selectionea',
  '/josaaea-members',
  '/tnea-simulator',
  '/conflict-assessment',
  '/internship-programs',
  '/contact-us',
  '/join-our-team',
];

const OUT_ROOT = path.resolve(__dirname, 'live_pages');
const HTML_DIR = path.join(OUT_ROOT, 'html');
const TEXT_DIR = path.join(OUT_ROOT, 'text');
const SHOT_DIR = path.join(OUT_ROOT, 'screens');
const META_DIR = path.join(OUT_ROOT, 'meta');
for (const d of [HTML_DIR, TEXT_DIR, SHOT_DIR, META_DIR]) fs.mkdirSync(d, { recursive: true });

const slug = (p) => (p === '/' ? 'root' : p.replace(/^\//, '').replace(/\//g, '_') || 'root');

async function extractFrameDetails(frame) {
  try {
    return await frame.evaluate(() => {
      const title = document.title || '';
      const bodyText = (document.body?.innerText || '').trim();
      const links = Array.from(document.querySelectorAll('a[href]')).map((a) => ({
        text: (a.textContent || '').trim().replace(/\s+/g, ' '),
        href: a.getAttribute('href') || '',
      }));
      const forms = Array.from(document.querySelectorAll('form')).map((f) => ({
        action: f.getAttribute('action') || '',
        method: f.getAttribute('method') || '',
        fields: Array.from(f.querySelectorAll('input,select,textarea,button')).map((el) => ({
          tag: el.tagName.toLowerCase(),
          type: el.getAttribute('type') || '',
          name: el.getAttribute('name') || '',
          id: el.getAttribute('id') || '',
          placeholder: el.getAttribute('placeholder') || '',
          value: el.getAttribute('value') || '',
        })),
      }));
      const images = Array.from(document.querySelectorAll('img[src]')).map((img) => ({
        src: img.getAttribute('src') || '',
        alt: img.getAttribute('alt') || '',
      })).slice(0, 200);
      const scripts = Array.from(document.querySelectorAll('script')).map((s) => ({
        src: s.getAttribute('src') || '',
        inlineLen: (s.src ? 0 : (s.textContent || '').length),
      }));
      const headings = {
        h1: Array.from(document.querySelectorAll('h1')).map((h) => h.textContent?.trim()).filter(Boolean),
        h2: Array.from(document.querySelectorAll('h2')).map((h) => h.textContent?.trim()).filter(Boolean),
        h3: Array.from(document.querySelectorAll('h3')).map((h) => h.textContent?.trim()).filter(Boolean),
      };
      return { title, bodyText, links, forms, images, scripts, headings };
    });
  } catch (e) {
    return { error: e.message };
  }
}

async function scrapeOne(context, pagePath) {
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push(e.message));

  const url = BASE + pagePath;
  const s = slug(pagePath);
  const started = Date.now();
  let status = 'unknown';
  try {
    const r = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 90000 });
    status = r ? r.status() : 'no-response';

    // Wait for slow content to render
    await page.waitForTimeout(32000);
    try { await page.waitForLoadState('networkidle', { timeout: 15000 }); } catch (_) {}

    const outerHtml = await page.content();
    fs.writeFileSync(path.join(HTML_DIR, `${s}.html`), outerHtml);

    const outer = await extractFrameDetails(page.mainFrame());

    const frames = page.frames().filter((f) => f !== page.mainFrame());
    const frameResults = [];
    for (let i = 0; i < frames.length; i++) {
      const f = frames[i];
      const fUrl = f.url();
      let html = '';
      try { html = await f.content(); } catch (_) {}
      fs.writeFileSync(path.join(HTML_DIR, `${s}.frame-${i}.html`), html);
      const details = await extractFrameDetails(f);
      frameResults.push({ index: i, url: fUrl, ...details });
    }

    const combinedText = [outer.bodyText, ...frameResults.map((fr) => fr.bodyText || '')].join('\n\n---FRAME---\n\n');
    fs.writeFileSync(path.join(TEXT_DIR, `${s}.txt`), combinedText);

    fs.writeFileSync(
      path.join(META_DIR, `${s}.json`),
      JSON.stringify(
        {
          path: pagePath,
          url,
          status,
          title: outer.title,
          outer,
          frames: frameResults,
          pageErrors: errors,
          tookMs: Date.now() - started,
        },
        null,
        2
      )
    );

    await page.screenshot({
      path: path.join(SHOT_DIR, `${s}.png`),
      fullPage: true,
      timeout: 45000,
    }).catch(() => {});

    const totalText = combinedText.length;
    const totalForms = (outer.forms?.length || 0) + frameResults.reduce((a, fr) => a + (fr.forms?.length || 0), 0);
    console.log(`OK  ${pagePath}  status=${status}  frames=${frameResults.length}  text=${totalText}  forms=${totalForms}`);
  } catch (e) {
    console.log(`ERR ${pagePath}  ${e.message.split('\n')[0]}`);
    fs.writeFileSync(
      path.join(META_DIR, `${s}.json`),
      JSON.stringify({ path: pagePath, url, error: e.message }, null, 2)
    );
  } finally {
    await page.close().catch(() => {});
  }
}

async function main() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    userAgent:
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
  });

  const concurrency = 4;
  let idx = 0;
  async function worker(id) {
    while (idx < PATHS.length) {
      const my = idx++;
      const p = PATHS[my];
      console.log(`[w${id}] -> ${p} (${my + 1}/${PATHS.length})`);
      await scrapeOne(context, p);
    }
  }
  await Promise.all(Array.from({ length: concurrency }, (_, i) => worker(i + 1)));

  await browser.close();
  console.log('Done. Files saved under reference/live_pages/{html,text,screens,meta}/');
}

main().catch((e) => {
  console.error('FATAL', e);
  process.exit(1);
});
