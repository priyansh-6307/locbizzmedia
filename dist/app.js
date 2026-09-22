const menuButton=document.querySelector('.menu-toggle');
const menu=document.querySelector('.menu');
const main=document.querySelector('main');
const footer=document.querySelector('footer');
function toggleMenu(open){
  menuButton.setAttribute('aria-expanded',String(open));
  menuButton.setAttribute('aria-label',open?'Close menu':'Open menu');
  menu.hidden=!open; main.inert=open; if(footer)footer.inert=open;
  document.body.classList.toggle('locked',open);
  if(open)menu.querySelector('a').focus();else menuButton.focus();
}
menuButton.addEventListener('click',()=>toggleMenu(menu.hidden));
document.addEventListener('keydown',event=>{
  if(menu.hidden)return;
  if(event.key==='Escape')toggleMenu(false);
  if(event.key==='Tab'){
    const items=[menuButton,...menu.querySelectorAll('a')];
    const first=items[0],last=items.at(-1);
    if(event.shiftKey&&document.activeElement===first){event.preventDefault();last.focus()}
    else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first.focus()}
  }
});
const reducedMotion=matchMedia('(prefers-reduced-motion: reduce)').matches;
const hero=document.querySelector('.hero');
const ambientVideos=[...document.querySelectorAll('.reel-panel video,.about-hero video')];
const detailVideos=[...document.querySelectorAll('.kia-video-card video,.audi-video-card video')];
const reelWindow=document.querySelector('.reel-window');
const reelTrack=document.querySelector('.reel-track');
let motionPaused=reducedMotion;
let reelX=0,reelDragging=false,reelPointerId=null,reelDragStart=0,reelOrigin=0,reelLastFrame=performance.now();
const reelStart=()=>innerWidth>=1600?-280:innerWidth<=600?-190:-230;
const reelWidth=()=>reelTrack?.scrollWidth/2||0;
function wrapReel(){const start=reelStart(),width=reelWidth();if(!width)return;while(reelX<=start-width)reelX+=width;while(reelX>start)reelX-=width}
function renderReel(){if(reelTrack)reelTrack.style.transform=`translate3d(${reelX}px,0,0)`}
if(reelWindow&&reelTrack){
  reelTrack.style.animation='none';reelX=reelStart();renderReel();reelWindow.style.touchAction='pan-y';
  const endDrag=event=>{if(!reelDragging||event.pointerId!==reelPointerId)return;reelDragging=false;reelWindow.classList.remove('dragging');if(reelWindow.hasPointerCapture(event.pointerId))reelWindow.releasePointerCapture(event.pointerId);reelPointerId=null};
  reelWindow.addEventListener('pointerdown',event=>{if(event.target.closest('a,button'))return;reelDragging=true;reelPointerId=event.pointerId;reelDragStart=event.clientX;reelOrigin=reelX;reelWindow.classList.add('dragging');reelWindow.setPointerCapture(event.pointerId)});
  reelWindow.addEventListener('pointermove',event=>{if(!reelDragging||event.pointerId!==reelPointerId)return;event.preventDefault();reelX=reelOrigin+event.clientX-reelDragStart;wrapReel();renderReel()});
  reelWindow.addEventListener('pointerup',endDrag);reelWindow.addEventListener('pointercancel',endDrag);reelWindow.addEventListener('lostpointercapture',endDrag);
  const animateReel=now=>{const delta=Math.min((now-reelLastFrame)/1000,.05);reelLastFrame=now;if(!motionPaused&&!reelDragging){reelX-=reelWidth()/58*delta;wrapReel();renderReel()}requestAnimationFrame(animateReel)};
  requestAnimationFrame(animateReel);
}
function setMotion(paused){
  motionPaused=paused;hero?.classList.toggle('paused',paused);
  const button=document.querySelector('.motion-toggle');
  if(button){button.textContent=paused?'PLAY MOTION':'PAUSE MOTION';button.setAttribute('aria-pressed',String(paused))}
  ambientVideos.forEach(video=>paused?video.pause():video.play().catch(()=>{}));
}
document.querySelector('.motion-toggle')?.addEventListener('click',()=>setMotion(!motionPaused));
setMotion(reducedMotion);
const mediaObserver=new IntersectionObserver(entries=>entries.forEach(({target,isIntersecting})=>{
  if(!isIntersecting)target.pause();else if(!motionPaused)target.play().catch(()=>{});
}),{threshold:.1});
ambientVideos.forEach(video=>mediaObserver.observe(video));
const detailObserver=new IntersectionObserver(entries=>entries.forEach(({target,isIntersecting})=>{
  if(!isIntersecting)target.pause();else if(!reducedMotion)target.play().catch(()=>{});
}),{rootMargin:'180px 0px',threshold:.1});
detailVideos.forEach(video=>detailObserver.observe(video));
document.addEventListener('visibilitychange',()=>{
  if(document.hidden)document.querySelectorAll('video').forEach(video=>video.pause());
  else if(!motionPaused){
    [...ambientVideos,...detailVideos].forEach(video=>{const box=video.getBoundingClientRect();if(box.bottom>0&&box.top<innerHeight)video.play().catch(()=>{})});
  }
});
const projectData=JSON.parse(document.querySelector('#project-data').textContent);
const modal=document.querySelector('#project-modal');
const modalVideo=modal.querySelector('video');
let returnFocus;
document.querySelectorAll('.project-card').forEach(card=>{
  const video=card.querySelector('video');
  const start=()=>{if(reducedMotion)return;video.muted=true;video.play().then(()=>card.classList.add('previewing')).catch(()=>{})};
  const stop=()=>{video.pause();card.classList.remove('previewing')};
  card.addEventListener('pointerenter',start);card.addEventListener('pointerleave',stop);
  card.addEventListener('focus',start);card.addEventListener('blur',stop);
  card.addEventListener('click',()=>{
    stop();const project=projectData.find(item=>item.slug===card.dataset.project);
    if(project.route){location.href=project.route;return}
    returnFocus=card; modal.querySelector('h2').textContent=project.title;
    modal.querySelector('.modal-description').textContent=project.description;
    modal.querySelector('.modal-logo').src=project.logo;
    modal.querySelector('.modal-logo').alt=project.title+' logo';
    modal.querySelector('.modal-link').href=project.detailPath||('/projects/'+project.slug+'/');
    modal.querySelector('.modal-full').href=project.vimeo;
    modalVideo.src=project.video;modalVideo.poster=project.poster;modalVideo.muted=false;
    modal.showModal();document.body.classList.add('locked');modalVideo.play().catch(()=>{});
  });
});
modal.querySelector('.modal-close').addEventListener('click',()=>modal.close());
modal.addEventListener('click',event=>{if(event.target===modal)modal.close()});
modal.addEventListener('close',()=>{modalVideo.pause();modalVideo.removeAttribute('src');modalVideo.load();document.body.classList.remove('locked');returnFocus?.focus()});
function filterProjects(category){
  const known=['all','automotive','gaming','product'];if(!known.includes(category))category='all';
  let count=0;
  document.querySelectorAll('.projects-page .project-card').forEach(card=>{card.hidden=category!=='all'&&card.dataset.category!==category;if(!card.hidden)count++});
  document.querySelectorAll('.filters a').forEach(link=>link.setAttribute('aria-current',String(link.dataset.filter===category)));
  const status=document.querySelector('.filter-count');if(status)status.textContent=count+' project'+(count===1?'':'s');
}
document.querySelectorAll('.filters a').forEach(link=>link.addEventListener('click',event=>{event.preventDefault();history.pushState({},'',link.href);filterProjects(link.dataset.filter)}));
window.addEventListener('popstate',()=>filterProjects(new URLSearchParams(location.search).get('category')||'all'));
filterProjects(new URLSearchParams(location.search).get('category')||'all');
document.querySelectorAll('form.inquiry').forEach(form=>form.addEventListener('submit',event=>{
  event.preventDefault();if(!form.reportValidity())return;
  const data=new FormData(form);
  const subject=encodeURIComponent('LOCBIZZ project inquiry — '+data.get('name'));
  const body=encodeURIComponent('Name: '+data.get('name')+'\nEmail: '+data.get('email')+'\n\n'+data.get('message'));
  const url='mailto:priyanshyadav364@gmail.com?subject='+subject+'&body='+body;
  form.querySelector('.form-note').textContent='Your email app will open with your inquiry. Review it and press Send there. You can also email priyanshyadav364@gmail.com directly.';
  window.location.href=url;
}));
