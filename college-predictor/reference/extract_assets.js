/**
 * Split each scraped iframe HTML file into:
 *   reference/live_pages/extracted/<slug>/body.html     (DOM without <style>/<script>)
 *   reference/live_pages/extracted/<slug>/styles.css    (all inline <style> blocks combined)
 *   reference/live_pages/extracted/<slug>/scripts.js    (all inline <script> blocks combined)
 *   reference/live_pages/extracted/<slug>/external.json (external CSS hrefs and JS src URLs)
 */
const fs = require('fs');
const path = require('path');
const { JSDOM } = (() => {
  try { return require('jsdom'); } catch { return { JSDOM: null }; }
})();

const ROOT = path.resolve(__dirname, 'live_pages');
const HTML_DIR = path.join(ROOT, 'html');
const OUT = path.join(ROOT, 'extracted');
fs.mkdirSync(OUT, { recursive: true });

function splitHtml(html) {
  const styles = [];
  const scripts = [];
  const externalCss = [];
  const externalJs = [];

  // Collect external <link rel="stylesheet"> via regex (light-weight, no DOM needed)
  const linkRe = /<link\b[^>]*rel=["']?stylesheet["']?[^>]*>/gi;
  for (const m of html.matchAll(linkRe)) {
    const hrefMatch = m[0].match(/href=["']([^"']+)["']/i);
    if (hrefMatch) externalCss.push(hrefMatch[1]);
  }

  // Extract <style>...</style>
  let stripped = html.replace(/<style\b[^>]*>([\s\S]*?)<\/style>/gi, (_, css) => {
    styles.push(css);
    return '';
  });

  // Extract <script>...</script>
  stripped = stripped.replace(/<script\b([^>]*)>([\s\S]*?)<\/script>/gi, (_, attrs, js) => {
    const srcMatch = attrs.match(/src=["']([^"']+)["']/i);
    if (srcMatch) externalJs.push(srcMatch[1]);
    else if (js.trim()) scripts.push(js);
    return '';
  });

  return { body: stripped, styles, scripts, externalCss, externalJs };
}

function processFile(file) {
  const slug = path.basename(file, '.html');
  const outDir = path.join(OUT, slug);
  fs.mkdirSync(outDir, { recursive: true });

  const full = fs.readFileSync(path.join(HTML_DIR, file), 'utf8');
  const { body, styles, scripts, externalCss, externalJs } = splitHtml(full);

  fs.writeFileSync(path.join(outDir, 'body.html'), body);
  fs.writeFileSync(path.join(outDir, 'styles.css'), styles.join('\n\n/* ---- next <style> block ---- */\n\n'));
  fs.writeFileSync(path.join(outDir, 'scripts.js'), scripts.join('\n\n// ---- next <script> block ----\n\n'));
  fs.writeFileSync(path.join(outDir, 'external.json'), JSON.stringify({ externalCss, externalJs }, null, 2));

  const stats = {
    slug,
    bodyBytes: Buffer.byteLength(body, 'utf8'),
    styleBlocks: styles.length,
    totalStyleBytes: styles.reduce((a, b) => a + Buffer.byteLength(b, 'utf8'), 0),
    scriptBlocks: scripts.length,
    totalScriptBytes: scripts.reduce((a, b) => a + Buffer.byteLength(b, 'utf8'), 0),
    externalCssCount: externalCss.length,
    externalJsCount: externalJs.length,
  };
  return stats;
}

function main() {
  const files = fs.readdirSync(HTML_DIR).filter((f) => f.endsWith('.html'));
  const stats = files.map(processFile);
  stats.sort((a, b) => b.totalStyleBytes + b.totalScriptBytes - (a.totalStyleBytes + a.totalScriptBytes));

  const lines = ['slug,bodyBytes,styleBlocks,styleBytes,scriptBlocks,scriptBytes,externalCss,externalJs'];
  for (const s of stats) lines.push([s.slug, s.bodyBytes, s.styleBlocks, s.totalStyleBytes, s.scriptBlocks, s.totalScriptBytes, s.externalCssCount, s.externalJsCount].join(','));
  fs.writeFileSync(path.join(OUT, 'index.csv'), lines.join('\n'));

  console.log('Extracted', files.length, 'files → reference/live_pages/extracted/');
  console.table(stats.slice(0, 15));
}

main();
