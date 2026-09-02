#!/usr/bin/env node
/**
 * qa.js - render a built guide and check it before it ships.
 *
 *   node qa.js guide.html                          # checks light and dark, prints a report
 *   node qa.js one-sheet.html --pdf out.pdf --pages 2
 *
 * Checks:
 *   - renders with no console errors and no failed network requests
 *   - no horizontal overflow at 390px (phone) or 1280px (laptop)
 *   - light and dark themes both paint a real background
 *   - optional PDF export with a hard page-count assertion
 *
 * Requires playwright or puppeteer. Exits non-zero on any failure.
 */

const path = require('path');

function globalRoot() {
  try {
    return require('child_process').execSync('npm root -g', { stdio: ['ignore', 'pipe', 'ignore'] })
      .toString().trim();
  } catch (_) { return null; }
}

async function loadDriver() {
  const root = globalRoot();
  for (const name of ['playwright', 'puppeteer']) {
    const kind = name;
    try { return { kind, mod: require(name) }; } catch (_) {}
    if (root) {
      try { return { kind, mod: require(path.join(root, name)) }; } catch (_) {}
    }
  }
  console.error('ERROR: install one of:  npm i -D playwright   |   npm i -D puppeteer');
  process.exit(2);
}

function parseArgs(argv) {
  const args = { file: null, pdf: null, pages: null };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--pdf') args.pdf = argv[++i];
    else if (a === '--pages') args.pages = parseInt(argv[++i], 10);
    else if (!args.file) args.file = a;
  }
  return args;
}

(async () => {
  const args = parseArgs(process.argv);
  if (!args.file) {
    console.error('usage: node qa.js <file.html> [--pdf out.pdf] [--pages N]');
    process.exit(1);
  }
  const url = 'file://' + path.resolve(args.file);
  const { kind, mod } = await loadDriver();
  const failures = [];

  const browser = kind === 'playwright'
    ? await mod.chromium.launch()
    : await mod.launch({ args: ['--no-sandbox'] });

  for (const scheme of ['light', 'dark']) {
    for (const [label, width] of [['phone', 390], ['laptop', 1280]]) {
      const page = kind === 'playwright'
        ? await (await browser.newContext({ colorScheme: scheme, viewport: { width, height: 900 } })).newPage()
        : await browser.newPage();

      if (kind === 'puppeteer') {
        await page.setViewport({ width, height: 900 });
        await page.emulateMediaFeatures([{ name: 'prefers-color-scheme', value: scheme }]);
      }

      page.on('console', (m) => {
        if (m.type() === 'error') failures.push(`[${scheme}/${label}] console error: ${m.text()}`);
      });
      page.on('requestfailed', (r) => {
        failures.push(`[${scheme}/${label}] failed request: ${r.url()}`);
      });

      await page.goto(url, { waitUntil: 'load' });

      const info = await page.evaluate(() => ({
        scrollW: document.documentElement.scrollWidth,
        clientW: document.documentElement.clientWidth,
        bodyBg: getComputedStyle(document.body).backgroundColor,
        color: getComputedStyle(document.body).color,
        sections: document.querySelectorAll('section, .section').length,
      }));

      if (info.scrollW > info.clientW + 1) {
        failures.push(`[${scheme}/${label}] horizontal overflow: ${info.scrollW}px in ${info.clientW}px`);
      }
      if (info.bodyBg === 'rgba(0, 0, 0, 0)' || info.bodyBg === 'transparent') {
        failures.push(`[${scheme}/${label}] body has no explicit background, it will borrow the host theme`);
      }
      console.log(`[${scheme}/${label}] bg=${info.bodyBg} color=${info.color} sections=${info.sections}`);
      if (info.sections > 6) {
        failures.push(`section cap exceeded: ${info.sections} found, 6 allowed`);
      }
      await page.close();
    }
  }

  if (args.pdf) {
    const page = kind === 'playwright'
      ? await (await browser.newContext()).newPage()
      : await browser.newPage();
    await page.goto(url, { waitUntil: 'load' });
    if (kind === 'playwright') await page.emulateMedia({ media: 'print' });
    else await page.emulateMediaType('print');
    await page.pdf({ path: args.pdf, format: 'Letter', printBackground: false,
                     margin: { top: '0.45in', bottom: '0.45in', left: '0.45in', right: '0.45in' } });
    await page.close();

    if (args.pages) {
      const buf = require('fs').readFileSync(args.pdf);
      const count = (buf.toString('latin1').match(/\/Type\s*\/Page[^s]/g) || []).length;
      console.log(`pdf pages: ${count} (max: ${args.pages})`);
      if (count > args.pages) {
        failures.push(`PDF is ${count} pages, max is ${args.pages}. Cut content, do not shrink the font below 9pt.`);
      } else if (count < args.pages) {
        console.log(`NOTE: ${count} page(s), under the ${args.pages}-page budget. Room for one more trap or worked problem.`);
      }
    }
  }

  await browser.close();

  if (failures.length) {
    console.error('\nFAILED:');
    failures.forEach((f) => console.error('  - ' + f));
    process.exit(1);
  }
  console.log('\nPASS');
})();
