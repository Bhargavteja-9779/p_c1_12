const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({userAgent:'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'});
  for (const u of process.argv.slice(2)) {
    try { await p.goto(u,{waitUntil:'domcontentloaded',timeout:45000}); await p.waitForTimeout(6000);
      const t = await p.innerText('body'); console.log('=== '+u+'\n'+t.slice(0,4000)); } catch(e){ console.log('ERR '+u+' '+e.message.slice(0,100)); }
  }
  await b.close();
})();
