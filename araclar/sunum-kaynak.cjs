// 14 slaytin duzenlenebilir HTML kaynagini ve yerel onizlemesini uretir.
// Dosya kimlikleri korunur. Uzak sunuma yayinlama islemi yapmaz.
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..', 'rehber', 'sunum');
const ink='#16202A',muted='#495660',paper='#F5F3EE',accent='#B4410F',teal='#17685F';
const esc=s=>s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
const p=(text,size=36,color=muted,extra='')=>`<p style="margin:0;font-size:${size}px;line-height:1.42;color:${color};${extra}">${text}</p>`;
const h=(text,size=43)=>`<h3 style="margin:0;font-size:${size}px;line-height:1.18;font-weight:600">${text}</h3>`;
const col=(html,extra='')=>`<div style="display:flex;flex-direction:column;gap:24px;${extra}">${html}</div>`;
const row=(label,body)=>`<div style="display:grid;grid-template-columns:460px 1fr;gap:56px;padding:28px 0;border-top:1px solid #D1CBBF">${h(label,36)}${p(body,32)}</div>`;
const table=(headers,rows,widths)=>`<table style="width:100%;table-layout:fixed;border-collapse:collapse;font-size:30px;line-height:1.32;text-align:left"><colgroup>${widths.map(w=>`<col style="width:${w}%">`).join('')}</colgroup><thead><tr>${headers.map(t=>`<th style="padding:0 26px 22px 0;border-bottom:2px solid #B8B1A5;font-size:25px;color:${accent};font-weight:600">${t}</th>`).join('')}</tr></thead><tbody>${rows.map(cells=>`<tr>${cells.map(t=>`<td style="padding:25px 26px 25px 0;border-bottom:1px solid #D1CBBF;vertical-align:top">${t}</td>`).join('')}</tr>`).join('')}</tbody></table>`;
const slides=[
 {
  id:'kapak',title:'Sağlayıcıdan bağımsız<br>ikinci beyin',dark:true,cover:true,
  body:p('Model değişir. Uygulama değişir.<br>Taşınan bilgi kalır.',56,'#EDE9E1','max-width:1450px')+p('Playground denemesi<br>20 Eylül 2026',27,'#ADB8C1','margin-top:52px'),
  note:'Bu yapı, bir sohbet uygulamasının kendi hafızasına bağlı kalmadan kararları ve gerekçeleri sonraki çalışma oturumuna taşımayı amaçlar. Burada ölçülmüş uygulamalar Claude Code ve Codex. Başka uygulamaların aynı refleksleri gösterdiği varsayılmaz. Kaynak: AGENTS.md; notlar/ikinci-beyin-mimarisi.md; notlar/kullanici-baglami.md, “Bu beynin amacı”.'
 },
 {
  id:'parcalar',title:'Yeniden anlatma sorunu',
  body:`<div style="display:grid;grid-template-columns:1fr 1fr;gap:100px">${col(p('OTURUM DEĞİŞTİĞİNDE',25,accent)+h('İş sürer.<br>Bağlam kesilir.',58)+p('Yeni ajan önceki kararın nedenini bilmeyebilir. Elenen yolu yeniden dener; açık işi gözden kaçırır.',38))}${col(p('BU KLASÖRÜN İŞİ',25,teal)+h('Devam edilecek<br>bir kayıt bırakmak',58)+p('Sonraki ajan gerekli bilgiyi okur, kaynağına gider ve kaldığın yerden çalışır.',38))}</div>`+p('Kazanç: aynı işi yeniden açıklamak ve aynı hatayı yeniden keşfetmek için daha az emek.',31,muted,'margin-top:68px;max-width:1600px'),
  note:'Bu, ölçülmüş bir zaman tasarrufu yüzdesi iddiası değildir; sistemin çözmeyi hedeflediği kullanıcı sorunudur. Canlı sohbet bağlamı her model/uygulama arasında kendiliğinden paylaşılmaz. Paylaşılan şey dosyalardır. Kaynak: notlar/iki-ajan-calismasi.md, “Ortak olan dosyalardır, bağlam değil”; notlar/kapanis-ritueli.md.'
 },
 {
  id:'ilke',title:'Bir sonraki oturuma kalan bilgi',
  body:row('Karar ve gerekçesi','Ne seçtik, hangi ihtiyaca cevap veriyor? Gerekçe, aynı kararı yeniden tartışmayı önler.')+row('Deneme ve karşı kanıt','Ne denedik, neden eledik? Başarısız yol da tekrar etmeyi önleyen bilgidir.')+row('Açık iş ve kaynak','Ne eksik, nereden devam edilir? Tarih ve oturum adresi iddiayı yeniden incelemeyi sağlar.'),
  note:'AGENTS.md kapanışta bu üç soruyu zorunlu tutar; sabit bir boş şablon dayatmaz. Kalıcı notlara ölçüm, karar ve elenen fikir terfi eder. Günlük konuşmanın tamamı aynı ağırlıkta sıcak bağlama taşınmaz. Kaynak: AGENTS.md “Oturum kapanışı”; notlar/ikinci-beyin-mimarisi.md.'
 },
 {
  id:'claude',title:'Tek ortak hafıza',
  body:table(['Bu klasöre gelen uygulama','Ortak bilgiyi kullanma yolu'],[
   ['Claude Code','CLAUDE.md üzerinden ortak kuralları ve konu notlarını okur.'],
   ['Codex CLI / Desktop','AGENTS.md üzerinden aynı haritayı ve konu notlarını okur.'],
   ['Antigravity, yerel modeller, diğerleri','Yerel erişim ve adaptör sınanmalı. Bu klasörde otomatik davranışları <b>ölçülmedi</b>.']
  ],[36,64])+p('Ortak çekirdek: kurallar, Markdown notlar, arşiv ve araçlar.<br>Uygulamaya özel parça: bunları ne zaman çağırdığı ve kayıt biçimi.',36,ink,'margin-top:48px'),
  note:'Anthropic/OpenAI sağlayıcı, model ve uygulama aynı kavram değildir. Antigravity bir uygulama örneğidir; burada bir sağlayıcı diye sınıflandırılmıyor. Bağımsızlık, her uygulamanın otomatik olarak aynı yeteneğe sahip olması demek değildir. Kaynak: AGENTS.md; CLAUDE.md; rehber/uygulama-adaptorleri.md; araclar/kayit.py.'
 },
 {
  id:'codex',title:'Bilgi neden dosyalarda?',
  body:`<div style="display:grid;grid-template-columns:1.12fr 1fr;gap:100px">${col(h('Sahip olduğun<br>okunabilir kayıt',60)+p('Kararı bir uygulamanın kapalı hafızasına bırakmak yerine, kendi klasöründe metin olarak tutarsın.',39))}${col(h('Markdown',36)+p('İnsan da ajan da okuyabilir ve düzenleyebilir.',32)+h('Bağlar ve kaynaklar',36)+p('İlgili notu ve kararın doğduğu konuşmayı bulmayı sağlar.',32)+h('Git ve Obsidian',36)+p('Git geçmişi korur. Obsidian dosyaları ve bağları gösterir.',32))}</div>`+p('Bilgi taşınabilir; kayıt yolları, izinler ve uygulama adaptörleri yeni ortamda ayrıca doğrulanır.',29,muted,'margin-top:64px'),
  note:'Obsidian bir görüntüleyicidir; bağlar dosyaların içindedir. Git commit yerel geri dönüş noktasıdır, uzak yedek için ayrıca başarılı push gerekir. Klasör taşınması ham kayıtların eski yol anahtarlarıyla ilişkisini bozabilir; sadece klasörü taşımak bütün otomasyonu taşımaz. Kaynak: notlar/ikinci-beyin-mimarisi.md “Obsidian’ın yeri”; notlar/gece-derleyicisi.md; BEYIN.md taşınma notu.'
 },
 {
  id:'diger',title:'İki bilgi katmanı, bir giriş haritası',
  body:row('BEYIN.md','Giriş ve yön bulma: hangi konu hangi dosyada, sıradaki iş nerede?')+row('notlar/','Güncel konu bilgisi: kararlar, yöntemler, ölçüm sınırları. Ajan haritadan gerekeni seçer.')+row('oturumlar/','Konuşmanın tarihçesi: ne yapıldı, ne değişti, neden? Gerektiğinde açılır.')+p('Ham konuşma günlüğünü uygulama kendi dizininde tutar.<br>Arşiv araçları buradan kanıt okur; bu günlük Markdown özetiyle aynı şey değildir.',31,ink,'margin-top:30px'),
  note:'65 KB seçmeli okuma ve 100 KB bakım eşiği mekanik işaretlerdir; not kalitesinin ölçüsü değildir. Kalıcı katman şu anda eşiğin üstünde. Arşiv geçmişi, kalıcı not güncel kararı taşır; önceki iddiaya sonraki karşı kanıtla birlikte bakılır. Kaynak: AGENTS.md; BEYIN.md; araclar/bakim.py; araclar/kayit.py.'
 },
 {
  id:'yasam',title:'Bir oturumun çalışma akışı',
  body:table(['An','Ajanın işi','Sende kalan kontrol'],[
   ['Başlangıç','Haritayı, gerekli konu notunu ve mevcut uyarıları okur.','Amacı ve sınırları belirtirsin.'],
   ['Çalışırken','Kararı, ölçümü ve açık işi çıktıkça diske yazar.','Gerekçeyi ve kaynağı sorgularsın.'],
   ['Anlamlı bir durakta','Ham kaydı okur; arşivi ve kalıcı notu günceller.','Kapanışı veya devri başlatırsın.'],
   ['Sonraki oturum','Aynı haritadan devam yerini bulur.','Eksik bağlam varsa kayda yönlendirirsin.']
  ],[19,51,30]),
  note:'Kapanış bütün kaydı ilk kez yazma anı olmamalıdır. Bulguların erken yazılması limit, kesinti ve bağlam kaybı riskini azaltır. Oturum kapandıktan sonra aynı görev yeniden sürerse kayıt hangi çalışma evresini kapsadığını söylemelidir. Kaynak: AGENTS.md; araclar/oturum-basi.md; oturumlar/2026-09-20-astra-kontrol.md.'
 },
 {
  id:'uyarilar',title:'Bir iddiayı kanıtına bağlamak',
  body:`<div style="display:grid;grid-template-columns:1fr 1.15fr;gap:100px">${col(p('20 EYLÜL DENETİMİNDEN',25,accent)+h('81 mesaj<br>görünmüyordu',64)+p('“En büyük kayıt bütün konuşmayı içerir” varsayımı üç Codex oturumunda yanlış çıktı.',36))}${col(h('Ölçüm',37)+p('Aynı oturumun ham dosyaları karşılaştırıldı; küçük parçalardaki farklı mesajlar bulundu.',32)+h('Düzeltme',37)+p('Okuyucu parçaları birleştirdi. Asıl dosyalar yerinde kaldı.',32)+h('İz',37)+p('Sonuç, oturum kimliği ve zaman damgasıyla denetim kaydına bağlandı.',32))}</div>`+p('“Kapandı” bir iddiadır. Kayıt adresinin varlığı, iddianın içeriğinin doğru olduğunu tek başına kanıtlamaz.',30,muted,'margin-top:55px'),
  note:'Somut ölçüm 69 + 4 + 8 = 81 mesaj; birleşik mesaj sayıları 179, 21, 30. Kaynak: notlar/astra-denetim-bulgulari.md; oturumlar/2026-09-20-astra-kontrol.md 04:22; derleme/astra-kontrol/ilk-olcum.json ve ilgili ham parça karşılaştırması. İşaretçi denetimi yalnız kaynağın/damganın bulunduğunu kontrol eder, semantik doğruluğu değil. Örnek kaynak adresi: (codex 01a0bc5c-f1c4 · 20.09 04:22).'
 },
 {
  id:'cumleler',title:'Yeni bir uygulamayı bağlamak',
  body:row('Ön koşul','Yerel dosyaları okuyabiliyor mu? Komut çalıştırabiliyor mu? Eksik yetenek açıkça yazılır.')+row('İlk temas','Ortak kuralları ve haritayı tanır. Kalıcı talimat yoksa başlangıç mesajını her oturumda kullanıcı verir.')+row('Adaptör ve sınama','Kayıt okuyucusu ve varsa hook bağlanır. Temiz bir oturumda gerçek çıktı türüyle doğrulanır.')+p('Belirsiz olan “ölçülmedi” kalır. Modelin “çalışıyor” demesi otomatik çalışmanın kanıtı değildir.',32,ink,'margin-top:30px'),
  note:'Sekiz adımlı ayrıntı rehber/uygulama-adaptorleri.md içinde. Kullanıcı hook güvenini verir; ajan bunu varsaymaz. Yerel dosya erişimi olan ama komut çalıştıramayan uygulama sınırlı okuma yapabilir. Kapalı sohbetlerin konuşmasını bu klasöre otomatik yakalayan evrensel köprü kurulmadı. Antigravity entegrasyonu yerelde ölçülmedi.'
 },
 {
  id:'kapanis',title:'Kapanışta bilgi aktarımı',
  body:`<div style="display:grid;grid-template-columns:1fr 1fr;gap:90px">${col(p('ÖNCE KAYIT',25,accent)+h('Oturumun omurgası',52)+p('Ajan kesin kimlikle ham konuşmayı okur. Son konuşulan konuyu bütün oturum sanmaz.',35)+p('<span style="font-family:\'JetBrains Mono\',monospace">omurga.py &lt;kesin kimlik&gt;</span>',27,muted))}${col(p('SONRA İKİ ÇIKTI',25,teal)+h('Arşiv ve kalıcı not',52)+p('Arşiv, o oturumun akışını korur. Kalıcı not, sonraki işte kullanılacak kararı ve gerekçeyi taşır.',35)+p('Harita, bağlar ve kaynak adresleri birlikte güncellenir.',30,muted))}</div>`+p('Kapanış işareti gerçek kapanış onayına bağlıdır.<br>Gece taslağı ve compact kurtarması tek başına oturumu kapatmaz.',35,ink,'margin-top:58px'),
  note:'Normal omurga gerçek kullanıcı mesajlarını; --tam modelin metin yanıtlarını da taşır. Araç çıktıları ve düşünme blokları omurgada yoktur; ayrıntı gerekiyorsa ham kayıt incelenir. Karar/neden, elenen yol ve açık iş kayıtta bulunur. Kaynak: AGENTS.md; araclar/omurga.py; araclar/kayit.py. Kapanış işareti kapanan-oturum: ve kesin/benzersiz kimliktir.'
 },
 {
  id:'gece',title:'Otomasyonun görevleri ve sınırları',
  body:table(['Tetik','Yaptığı iş','Sınırı'],[
   ['Oturum başlangıcı','Harita, kimlik ve mevcut uyarıları getirir.','Uygulama desteği ve güven ayarı gerekir.'],
   ['Yeni kullanıcı mesajı','%50 / %70 dolulukta uyarır, kurtarma kaydı alır.','Uzun tek turun içinde sürekli denetim yok.'],
   ['Compact öncesi','Konuşma omurgasını kurtarmaya çalışır.','Codex’te canlı zincir ölçülmedi.'],
   ['Gece 00:30 görevi','Açıkları tarar, uygun oturuma taslak üretir, commit/push dener.','Yeni görev ayarının gece sonucu ölçülmedi.']
  ],[22,44,34]),
  note:'Gerçek %50/%70 Claude ve Codex kayıtlarında görüldü. Codex ölçümleri eski 258.400 penceredeydi; son etkin pencere 828.400, yeni pencerenin eşik/compact geçişi ölçülmedi. Gece taslağı: kapanışsız, en az 6 saat sessiz, uygun oturum; gece başına en fazla 3. Model notlara otomatik terfi yapmaz. Görev için açık kullanıcı oturumu ve priz gerekir; telafi açık, uyandırma kapalı. Kaynak: araclar/baglam.py, gece_kayit.py, derle.py; onaylı görev ayarı; notlar/astra-denetim-bulgulari.md.'
 },
 {
  id:'sinirlar',title:'Bugünkü kanıt durumu',
  body:table(['Özellik','Durum','Bu durum neyi kapsar?'],[
   ['Ortak notları kullanma','Ölçüldü','Claude Code ve Codex; aynı dosyalar, ayrı canlı bağlam.'],
   ['Codex %50 / %70 uyarısı','Canlı ölçüldü','İki kullanıcı mesajında hook ve kurtarma dosyası.'],
   ['Gece görevinin yeni ayarı','Kuru test geçti','Yeni zamanlı çalışmanın tamamı ölçülmedi.'],
   ['Codex PreCompact','Ölçülmedi','Kod ve adaptör var; canlı olayın kanıtı yok.'],
   ['Antigravity / diğer uygulamalar','Ölçülmedi','Tanıtma protokolü var; eşdeğer otomasyon varsayılmaz.']
  ],[32,22,46])+p('Claude pencere büyüklüğü kalibrasyona dayanıyor. Kapalı sohbetlerin otomatik yakalanması da açık bir iş.',28,muted,'margin-top:32px'),
  note:'Durum 20.09.2026 yerel ölçümlerine aittir; sürüm değişince yeniden sınanır. Eşit hafıza garantisi verilmez. Görev çalıştı/çalışmadı ayrımı LastTaskResult, son-calisma.json, günlük ve git ile ölçülür; model beyanı veya ayar dosyası tek başına kanıt olmaz. Kaynak: rehber/uygulama-adaptorleri.md; oturumlar/2026-09-20-astra-kontrol.md 1–16 matrisi; notlar/capraz-arac-baglam.md.'
 },
 {
  id:'komutlar',title:'Bilgi biriktikçe bakım gerekir',
  body:row('Güncel çekirdek küçük kalır','Büyük notu sadece iki dosyaya bölmek yetmez. Eski ölçüm dökümü arşivde, geçerli yöntem konu notunda kalır.')+row('Geçmiş ve karşı kanıt korunur','Yanlışlanan iddia, düzeltmesinden koparılmaz. Kaynak bağlantıları yeni yerinde de çalışır.')+row('Yetki sınırı görünür kalır','Dosya taşıma, silme ve sistem ayarı kullanıcı onayı ister. Test verisi kendi geçici alanında temizlenir.')+p('Kalıcı katman 100 KB bakım eşiğini aşıyor. Bölme planı hazır; not budaması henüz uygulanmadı.',31,ink,'margin-top:30px'),
  note:'128,5 KB ölçümü ve yaklaşık 96 KB önerisi rehber/kalici-katman-bakim-plani.md içinde; bu bir hedef, sonuç değil. Dosya isimleri, kararlar ve kaynaklar korunarak soğuk katmana taşıma öneriliyor. Kimlik numarası, parola ve mali detay projeye yazılmaz. Testlerin TemporaryDirectory temizliği 28 testle ve sıfır yeni kalıntıyla sınandı; eski 178 klasörün silinmesi ayrı işlemdir.'
 },
 {
  id:'son',title:'Sonraki oturumun başlangıç noktası',dark:true,
  body:p('“Haritayı ve ilgili notu oku.<br>Açık işi, gerekçesiyle devam ettir.”',61,'#EDE9E1','max-width:1580px')+p('Bu denemenin başarısı, yeni gelen ajanın<br>geçmiş kararı bulup kaynağıyla doğru kullanabilmesidir.',39,'#B9C3CC','max-width:1560px;margin-top:68px')+p('Model ve uygulama değişebilir.<br>Bilginin sürekliliği, bu okuma ve yazma düzenine dayanır.',33,'#E3A66D','margin-top:48px'),
  note:'Bu kapanış bir tamamlanmış evrensel hafıza garantisi değildir; sistemin başarı ölçütüdür. Giriş BEYIN.md, uygulanan ortak kural AGENTS.md. Ayrıntılı araçlar ve uygulama farkları rehber/codex-sunum-rehberi.md ile rehber/uygulama-adaptorleri.md içinde. Amaç bütün ham geçmişi her oturuma yüklemek değil, gerekli karara ve kaynağına ulaşmaktır.'
 }
];

for(let i=0;i<slides.length;i++){
 const s=slides[i];const bg=s.dark?ink:paper;const fg=s.dark?'#EDE9E1':ink;
 const html=`<section id="${s.id}" data-transition="fade" aria-label="${i+1}. ${s.title.replaceAll('<br>',' ')}" style="box-sizing:border-box;position:relative;width:1920px;height:1080px;overflow:hidden;background:${bg};color:${fg};font-family:'IBM Plex Sans',Arial,sans-serif;padding:108px 128px 115px;display:flex;flex-direction:column">
  <${s.cover?'h1':'h2'} style="margin:0 0 ${s.cover?'60':'64'}px;font-size:${s.cover?'100':'72'}px;font-weight:600;line-height:1.13;max-width:1660px">${s.title}</${s.cover?'h1':'h2'}>
  <div style="display:flex;flex-direction:column;gap:0">${s.body}</div>
  <p style="position:absolute;right:128px;bottom:48px;margin:0;font-size:24px;color:${s.dark?'#8797A3':'#707871'}">${String(i+1).padStart(2,'0')} / 14</p>
  <aside>${esc(s.note)}</aside>
</section>
`;
 fs.writeFileSync(path.join(root,'slides',s.id+'.html'),html);
}
const deck=JSON.parse(fs.readFileSync(path.join(root,'deck.json'),'utf8'));
deck.title='Sağlayıcıdan bağımsız ikinci beyin';
deck.order=slides.map(s=>s.id);
deck.sections={s1:{description:'Sorun, amaç ve sağlayıcıdan bağımsızlık',start:'kapak'},s2:{description:'Bilginin katmanları ve günlük çalışma',start:'diger'},s3:{description:'Adaptörler, kapanış ve otomasyon',start:'cumleler'},s4:{description:'Kanıt durumu, bakım ve devam',start:'sinirlar'}};
fs.writeFileSync(path.join(root,'deck.json'),JSON.stringify(deck,null,2)+'\n');
const fragments=slides.map(s=>fs.readFileSync(path.join(root,'slides',s.id+'.html'),'utf8')).join('\n');
const preview=`<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${deck.title}</title>
<style>*{box-sizing:border-box}body{margin:0;background:#D9D5CD}main{display:flex;flex-direction:column;align-items:center;gap:32px;padding:40px 0}section{flex-shrink:0;box-shadow:0 8px 24px #0001}aside{display:none}h1,h2,h3,p{margin:0}table{border-collapse:collapse}nav{position:sticky;top:0;z-index:5;background:#16202A;color:#EDE9E1;padding:14px 24px;font:16px Arial}nav a{color:#E3A66D;margin-right:20px}button{font:inherit;padding:7px 12px;margin-left:16px;cursor:pointer}.show-notes aside{display:block;position:absolute;inset:auto 128px 90px;background:#fff;color:#16202A;font-size:24px;padding:24px;line-height:1.4;box-shadow:0 0 0 2px #B4410F}@media print{nav{display:none}main{padding:0;gap:0}section{break-after:page;box-shadow:none}@page{size:1920px 1080px;margin:0}}</style></head><body><nav>Yerel kaynak önizlemesi <button id="notes">Konuşma notları</button> <span style="margin-left:20px">${slides.map((s,i)=>`<a href="#${s.id}">${i+1}</a>`).join('')}</span></nav><main>${fragments}</main><script>document.querySelector('#notes').onclick=()=>document.body.classList.toggle('show-notes');function size(){let scale=Math.min(1,(innerWidth-32)/1920);document.querySelector('main').style.zoom=scale}addEventListener('resize',size);size();</script></body></html>`;
fs.writeFileSync(path.join(root,'index.html'),preview);
const mapping=slides.map((s,i)=>`| ${i+1} | ${s.id} | ${s.title.replaceAll('<br>',' ')} |`).join('\n');
fs.writeFileSync(path.join(root,'KAYNAK.md'),`# Sunum kaynağı\n\n14 slayt, 1920 × 1080. Yerel önizleme: index.html. Yayındaki claude.ai kopyası bu işlemle değişmez.\n\nDüzenlenebilir içerik ve konuşma notları araclar/sunum-kaynak.cjs içinde. \`node araclar/sunum-kaynak.cjs\` HTML dosyalarını, deck.json ve önizlemeyi birlikte üretir. Dosya kimlikleri mevcut yayınla bağlantı kopmasın diye korundu; konu adları yeniden yazıldı.\n\n| Sıra | Kimlik | Konu |\n|---|---|---|\n${mapping}\n\nKaynaklar her slaydın aside konuşma notundadır. Ölçümler 20.09.2026 durumunu anlatır.\n`);
console.log('14 HTML slayti, deck.json, index.html ve kaynak haritasi yazildi.');
