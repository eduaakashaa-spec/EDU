const hamb=document.getElementById('hamb'),nl=document.getElementById('navlinks');
hamb.addEventListener('click',()=>nl.classList.toggle('show'));
nl.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>nl.classList.remove('show')));
document.querySelectorAll('.faq-item').forEach(it=>{
  it.querySelector('.faq-q').addEventListener('click',()=>it.classList.toggle('open'));
});
const io=new IntersectionObserver((es)=>{es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('visible');io.unobserve(e.target)}})},{threshold:.12});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));
