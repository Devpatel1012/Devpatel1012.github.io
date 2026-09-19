(function(){
  'use strict';
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var autoSelectors = ['.card', '.entry', '.pub', '.book', '.art-card', '.stat', '.notify-box'];
  var revealTargets = [];
  document.querySelectorAll(autoSelectors.join(',')).forEach(function(el){
    el.classList.add('reveal');
    revealTargets.push(el);
  });

  if(reduced || !('IntersectionObserver' in window)){
    revealTargets.forEach(function(el){ el.classList.add('visible'); });
    return;
  }

  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(entry){
      if(entry.isIntersecting){
        entry.target.classList.add('visible');
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.2, rootMargin: '0px 0px -6% 0px' });
  revealTargets.forEach(function(el){ io.observe(el); });
})();