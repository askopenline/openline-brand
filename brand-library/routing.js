export const ROUTES=['overview','logos','assets','ads','motion','presenters','app','guidelines','archives'];
export const routeParams=()=>new URLSearchParams(location.hash.startsWith('#/')?location.hash.split('?')[1]:location.search);
export function currentRoute(){
 const path=location.hash.startsWith('#/')?location.hash.slice(2).split('?')[0]:location.pathname.replace(/^\/|\/$/g,'');
 return !path||path==='index.html'?'overview':path;
}
export function routeURL(route,params=new URLSearchParams()){
 const query=params.toString();return '/'+route+(query?'?'+query:'');
}
export function normalizeRoute(){
 if(location.hash.startsWith('#/')){
  const route=location.hash.slice(2).split('?')[0]||'overview';
  if(ROUTES.includes(route)){
   const params=new URLSearchParams(location.search);
   for(const [k,v]of routeParams())params.set(k,v);
   history.replaceState(history.state,'',routeURL(route,params));
  }
 }else if(ROUTES.includes(currentRoute())&&location.pathname.endsWith('/')&&location.pathname!=='/'){
  history.replaceState(history.state,'',location.pathname.slice(0,-1)+location.search+location.hash);
 }
}
export function navigate(route,params=new URLSearchParams()){
 history.pushState(null,'',routeURL(route,params));window.dispatchEvent(new PopStateEvent('popstate'));
}
export function followRoute(event){
 if(event.defaultPrevented||event.button!==0||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey)return;
 const a=event.target.closest?.('a[href]');
 if(!a||a.hasAttribute('download')||(a.target&&a.target!=='_self'))return;
 const url=new URL(a.href);
 if(url.origin!==location.origin||url.hash||!ROUTES.includes(url.pathname.replace(/^\/|\/$/g,'')))return;
 event.preventDefault();navigate(url.pathname.replace(/^\/|\/$/g,''),url.searchParams);
}
