/* Shared, side-effect-free resolver used by the Safari extension. */
globalThis.ULRResolver=Object.freeze({
  collect(document,href,host){
    const urls=new Map();
    const add=a=>{if(!a)return;try{const u=new URL(a.getAttribute("href"),href);if(!["https:","http:"].includes(u.protocol)||u.username||u.password||u.href===href)return;urls.set(u.href,{url:u.href,label:(a.textContent||"Download").trim().slice(0,80)})}catch{}};
    if(/(^|\.)(vik1ngfile\.site|vikingfile\.com)$/.test(host))add(document.querySelector("#download-link[href]"));
    for(const a of document.querySelectorAll("a[download][href],a[href*='download'],a[href*='/api/file/']"))add(a);
    return [...urls.values()].slice(0,30);
  }
});
