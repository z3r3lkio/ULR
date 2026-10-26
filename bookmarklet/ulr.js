/* ULR Safari bookmarklet. Run manually after completing verification. */
(function(){
"use strict";
const host=location.hostname.toLowerCase();
const allowed=["vik1ngfile.site","vikingfile.com","mediafire.com","gofile.io","pixeldrain.com","1fichier.com"];
if(!allowed.some(d=>host===d||host.endsWith("."+d))){alert("ULR: unsupported host");return}
const items=new Map();
function add(anchor){if(!anchor)return;try{const u=new URL(anchor.getAttribute("href"),location.href);if(!["http:","https:"].includes(u.protocol)||u.username||u.password||u.href===location.href)return;items.set(u.href,u.href)}catch{}}
const preferred=/vik1ngfile|vikingfile/.test(host);
if(preferred)add(document.querySelector("#download-link[href]"));
for(const a of document.querySelectorAll("a[download][href],a[href*='download'],a[href*='/api/file/']"))add(a);
if(items.size===0){alert("ULR: no download link yet. Complete verification and run again.");return}
const urls=[...items.values()];
const chosen=urls.length===1?urls[0]:prompt("ULR: "+urls.length+" candidates. Enter number (1-"+urls.length+"):\n"+urls.map((u,i)=>(i+1)+": "+u).join("\n").slice(0,1500),"1");
if(chosen===null)return;
const index=urls.length===1?0:Number(chosen)-1;
if(!Number.isInteger(index)||index<0||index>=urls.length){alert("ULR: invalid selection");return}
prompt("ULR: copy this link:",urls[index]);
})();
