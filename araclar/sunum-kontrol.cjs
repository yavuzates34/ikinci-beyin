// Yerel HTML sunumunun goruntu ve tasma denetimi. Uzak hesaba yayinlamaz.
// NODE_PATH, Playwright modullerinin bulundugu dizini gosterebilir.
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const {chromium} = require('playwright');
const root = path.resolve(__dirname, '..');
const source = path.join(root, 'rehber', 'sunum');
const deck = JSON.parse(fs.readFileSync(path.join(source, 'deck.json'), 'utf8'));
const output = process.argv[2] || fs.mkdtempSync(path.join(os.tmpdir(), 'playground-sunum-'));
fs.mkdirSync(output, {recursive:true});
const styles = '*{box-sizing:border-box}body{margin:0}h1,h2,h3,p{margin:0}section{position:relative;width:1920px;height:1080px;overflow:hidden}aside{display:none}table{border-collapse:collapse}td,th{vertical-align:top}';
const fragments = deck.order.map(id => fs.readFileSync(path.join(source, 'slides', id+'.html'), 'utf8'));
async function main(){
 const browser = await chromium.launch({headless:true, executablePath:process.env.SUNUM_BROWSER || 'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 try {
  const page = await browser.newPage({viewport:{width:1920,height:1080},deviceScaleFactor:1});
  const checks=[];
  for(let i=0;i<fragments.length;i++){
   await page.setContent('<!doctype html><html lang="tr"><meta charset="utf-8"><style>'+styles+'</style><body>'+fragments[i]+'</body></html>');
   await page.screenshot({path:path.join(output,String(i+1).padStart(2,'0')+'.png')});
   const overflow=await page.evaluate(()=>{
    const section=document.querySelector('section'); const r=section.getBoundingClientRect();
    return Array.from(section.querySelectorAll('h1,h2,h3,p,td,th,li,div')).filter(el=>{
     const x=el.getBoundingClientRect();const css=getComputedStyle(el);
     return x.width && x.height && css.display!=='none' && (x.right>r.right+1||x.bottom>r.bottom+1||x.left<r.left-1||x.top<r.top-1||el.scrollWidth>el.clientWidth+2||el.scrollHeight>el.clientHeight+2);
    }).map(el=>({tag:el.tagName,text:el.textContent.trim().slice(0,110)}));
   });
   checks.push({slide:i+1,id:deck.order[i],overflow});
  }
  const thumbs=fragments.map((s,i)=>'<div class="cell"><div class="label">'+(i+1)+' '+deck.order[i]+'</div><div class="frame"><div class="inner">'+s+'</div></div></div>').join('');
  await page.setViewportSize({width:1430,height:Math.ceil(fragments.length/2)*425+24});
  await page.setContent('<!doctype html><html lang="tr"><meta charset="utf-8"><style>'+styles+'body{background:#dedbd4;padding:20px;display:grid;grid-template-columns:672px 672px;gap:20px}.label{font:16px Arial;margin-bottom:8px}.frame{width:672px;height:378px;overflow:hidden;background:white}.inner{transform:scale(.35);transform-origin:top left;width:1920px;height:1080px}</style><body>'+thumbs+'</body></html>');
  await page.screenshot({path:path.join(output,'overview.png'),fullPage:true});
  fs.writeFileSync(path.join(output,'checks.json'),JSON.stringify(checks,null,2));
  console.log(JSON.stringify({output,slideCount:checks.length,overflows:checks.filter(x=>x.overflow.length)},null,2));
 }finally {await browser.close();}
}
main().catch(e=>{console.error(e);process.exitCode=1;});
