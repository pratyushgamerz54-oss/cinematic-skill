// node tools/stills.js <url> <outprefix> t1 t2 ...  -> PNG stills at those times (window.__recordFrame)
const { chromium } = require('playwright');
(async () => {
  const [url, pre, ...ts] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
  p.on('console', m => { if (m.type() === 'error') console.log('console:', m.text()); });
  p.on('pageerror', e => console.log('pageerror:', e.message));
  await p.goto(url); await p.waitForFunction('window.__ready === true', null, { timeout: 120000 });
  for (const t of ts) { await p.evaluate(t => window.__recordFrame(+t), t); await p.screenshot({ path: `${pre}_${t}.png` }); }
  await b.close();
})();
