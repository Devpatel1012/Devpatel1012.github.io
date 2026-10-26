(function () {
  'use strict';
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Mobile drawer
  var toggle = document.querySelector('.mobile-toggle');
  var drawer = document.querySelector('.mobile-nav-drawer');
  function setDrawer(open) {
    if (!drawer || !toggle) return;
    drawer.classList.toggle('open', open);
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    toggle.textContent = open ? '\u2715' : '\u2630';
    document.body.style.overflow = open ? 'hidden' : '';
  }
  if (toggle) toggle.addEventListener('click', function () { setDrawer(!drawer.classList.contains('open')); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setDrawer(false); });
  if (drawer) drawer.addEventListener('click', function (e) { if (e.target.closest('a')) setDrawer(false); });

  // Toast + copy helpers
  function toast(msg) {
    var t = document.createElement('div');
    t.className = 'toast-feedback'; t.textContent = msg; t.setAttribute('role', 'status');
    document.body.appendChild(t);
    setTimeout(function () { t.remove(); }, 1800);
  }
  function copyText(text, msg) {
    var done = function () { toast(msg || 'Copied'); };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, function () { fallback(text); done(); });
    } else { fallback(text); done(); }
  }
  function fallback(text) {
    var ta = document.createElement('textarea'); ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
    document.body.appendChild(ta); ta.select(); try { document.execCommand('copy'); } catch (e) {} ta.remove();
  }
  document.querySelectorAll('[data-bibtex-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var el = document.getElementById(btn.getAttribute('data-bibtex-copy'));
      if (el) copyText(el.textContent, 'BibTeX copied');
    });
  });
  document.querySelectorAll('[data-bibtex-toggle]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var box = document.getElementById(btn.getAttribute('data-bibtex-toggle'));
      if (box) box.classList.toggle('open');
    });
  });
  document.querySelectorAll('.copy-cmd-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var code = btn.parentElement.querySelector('code');
      if (code) copyText(code.textContent, 'Command copied');
    });
  });

  // Project filters
  var filters = document.querySelectorAll('.filter-btn');
  filters.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var f = btn.getAttribute('data-filter');
      filters.forEach(function (b) { b.classList.toggle('active', b === btn); });
      document.querySelectorAll('.project-card').forEach(function (card) {
        var cats = (card.getAttribute('data-category') || '').split(' ');
        card.classList.toggle('hidden', f !== 'all' && cats.indexOf(f) === -1);
      });
    });
  });

  // Speaker waveform (illustration for the diarization work)
  document.querySelectorAll('[data-wave]').forEach(function (box) {
    var colors = ['#C8553D', '#7A9A7E', '#E9B44C'];
    var seg = [0,0,0,0,1,1,1,0,0,2,2,2,2,1,1,0,0,0,2,2,1,1,1,1,0,0,2,2,0,0,1,1];
    seg = seg.concat(seg.slice().reverse());
    seg.forEach(function (s, i) {
      var b = document.createElement('span');
      b.style.setProperty('--h', Math.min(100, 25 + Math.abs(Math.sin(i * 1.7) * 60) + (i % 3) * 6) + '%');
      b.style.setProperty('--c', colors[s]);
      b.style.setProperty('--d', (i % 8) * 0.12 + 's');
      box.appendChild(b);
    });
  });

  // Token packer illustration: 16x16 grid compresses to 8x8
  document.querySelectorAll('[data-tokgrid]').forEach(function (g) {
    var n = parseInt(g.getAttribute('data-tokgrid'), 10);
    for (var i = 0; i < n; i++) g.appendChild(document.createElement('b'));
  });

  // Scroll reveal
  var targets = document.querySelectorAll('.card, .letter, .book-row, .contact, .tl-item');
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.06 });
    targets.forEach(function (el) { el.classList.add('reveal'); io.observe(el); });
  }
})();
