/* Step-locked self-intro for the homepage.
   Each line has to finish "typing" (word by word) before the next one is
   reachable, and scrolling back up un-types it and steps back into the
   previous line -- fully reversible. Scroll/touch/keyboard input is captured
   while the intro is active so a fast scroll can't skip ahead in either
   direction. Once the last line finishes, the overlay unlocks and the real
   page scrolls normally. If JS never runs, the CSS default is plain static
   text -- nothing is hidden by default, so nobody gets stuck behind a broken
   lock. */
(function(){
  'use strict';
  var INTRO_KEY = 'devIntroShown';
  var overlay = document.querySelector('.intro-overlay');
  if(!overlay) return;

  function alreadySeen(){
    try{ return sessionStorage.getItem(INTRO_KEY) === '1'; }
    catch(err){ return false; } // storage blocked (private mode etc.) -- just play the intro
  }
  function markSeen(){
    try{ sessionStorage.setItem(INTRO_KEY, '1'); }
    catch(err){ /* ignore -- worst case it replays once more */ }
  }

  if(alreadySeen()){
    overlay.style.display = 'none';
    return;
  }

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(reduced){ markSeen(); return; }

  var inner = overlay.querySelector('.intro-inner');
  var lines = Array.prototype.slice.call(overlay.querySelectorAll('.intro-line'));
  var skipBtn = overlay.querySelector('.intro-skip');
  var n = lines.length;
  if(!n) return;

  /* Wrap each line's sentence into per-word spans so we can reveal them one
     at a time. Existing inline elements (highlight spans, the cursor, the
     handwritten aside) are left as single atomic units. */
  function wrapWords(p){
    var out = [];
    var frag = document.createDocumentFragment();
    Array.prototype.forEach.call(Array.prototype.slice.call(p.childNodes), function(node){
      if(node.nodeType === 3){
        var parts = node.textContent.split(/(\s+)/);
        parts.forEach(function(part){
          if(part === '') return;
          if(/^\s+$/.test(part)){ frag.appendChild(document.createTextNode(part)); return; }
          var span = document.createElement('span');
          span.className = 'word';
          span.textContent = part;
          frag.appendChild(span);
          out.push(span);
        });
      } else if(node.nodeType === 1){
        if(node.classList.contains('cursor')){ frag.appendChild(node); return; }
        node.classList.add('word');
        frag.appendChild(node);
        out.push(node);
      }
    });
    p.innerHTML = '';
    p.appendChild(frag);
    return out;
  }

  var lineWords = lines.map(function(line){
    var words = [];
    var p = line.querySelector('p');
    if(p){ words = words.concat(wrapWords(p)); }
    var scrawl = line.querySelector('.scrawl');
    if(scrawl){ words = words.concat(wrapWords(scrawl)); }
    return words;
  });

  /* Pacing: a fixed scroll budget PER WORD, so every line advances at the
     same rate regardless of how many words it has (a short line and a long
     line both feel equally "unhurried"). The last line gets extra scroll
     required before the intro finishes, so it doesn't unlock too abruptly.
     A single scroll/touch/key event can only ever contribute a capped
     amount, so no single motion -- forward or backward -- can skip a line. */
  var UNITS_PER_WORD = 34;
  var LAST_LINE_MULTIPLIER = 1.5;
  var MAX_EVENT_UNITS = 16;

  var lineUnits = lineWords.map(function(words, i){
    var total = Math.max(words.length, 1) * UNITS_PER_WORD;
    if(i === n - 1){ total *= LAST_LINE_MULTIPLIER; }
    return total;
  });

  var activeIdx = 0;
  var revealedUnits = 0;
  var finished = false;
  var touchStartY = null;

  overlay.classList.add('armed');
  lines[0].classList.add('active');
  document.documentElement.classList.add('intro-locked');

  function renderWords(idx, count){
    var words = lineWords[idx];
    for(var i = 0; i < words.length; i++){
      if(i < count){
        words[i].style.opacity = 1;
        words[i].style.transform = 'none';
        words[i].style.filter = 'none';
      } else {
        words[i].style.opacity = 0;
        words[i].style.transform = 'translateY(0.4em)';
        words[i].style.filter = 'blur(3px)';
      }
    }
  }

  function renderActiveLine(){
    var total = lineUnits[activeIdx];
    var words = lineWords[activeIdx];
    var fraction = Math.max(0, Math.min(1, revealedUnits / total));
    var wordsToShow = Math.ceil(fraction * words.length);
    renderWords(activeIdx, wordsToShow);
  }

  function scrollInnerToEnd(){
    if(inner.scrollHeight > inner.clientHeight){
      inner.scrollTo({ top: inner.scrollHeight, behavior: 'smooth' });
    }
  }

  function setHintVisible(visible){
    var hint = lines[0].querySelector('.intro-scrollhint');
    if(hint){ hint.style.opacity = visible ? 1 : 0; }
  }

  function completeCurrentLine(){
    lines[activeIdx].classList.remove('active');
    lines[activeIdx].classList.add('done', 'revealed');
    if(activeIdx < n - 1){
      activeIdx += 1;
      revealedUnits = 0;
      lines[activeIdx].classList.add('active');
      renderWords(activeIdx, 0);
      scrollInnerToEnd();
    } else {
      finished = true;
      setTimeout(unlockAndHide, 550);
    }
  }

  function advance(units){
    if(finished) return;
    setHintVisible(false);
    revealedUnits = Math.min(lineUnits[activeIdx], revealedUnits + units);
    renderActiveLine();
    scrollInnerToEnd();
    if(revealedUnits >= lineUnits[activeIdx]){
      completeCurrentLine();
    }
  }

  function reverse(units){
    if(finished) return;
    revealedUnits -= units;

    if(revealedUnits > 0){
      renderActiveLine();
      return;
    }

    if(activeIdx === 0){
      revealedUnits = 0;
      renderActiveLine();
      setHintVisible(true);
      return;
    }

    // Step back into the previous line, un-completing it.
    renderWords(activeIdx, 0);
    lines[activeIdx].classList.remove('active');
    activeIdx -= 1;
    lines[activeIdx].classList.remove('done', 'revealed');
    lines[activeIdx].classList.add('active');
    revealedUnits = Math.max(0, lineUnits[activeIdx] + revealedUnits);
    renderActiveLine();
    scrollInnerToEnd();
  }

  function unlockAndHide(){
    window.removeEventListener('wheel', onWheel, { passive:false });
    window.removeEventListener('touchstart', onTouchStart, { passive:true });
    window.removeEventListener('touchmove', onTouchMove, { passive:false });
    window.removeEventListener('keydown', onKey);
    if(skipBtn){ skipBtn.removeEventListener('click', onSkip); }
    document.documentElement.classList.remove('intro-locked');
    overlay.classList.add('exiting');
    markSeen();
    setTimeout(function(){ overlay.style.display = 'none'; }, 550);
  }

  function onWheel(e){
    e.preventDefault();
    var units = Math.max(2, Math.min(MAX_EVENT_UNITS, Math.abs(e.deltaY) / 4));
    if(e.deltaY > 0) advance(units);
    else if(e.deltaY < 0) reverse(units);
  }
  function onTouchStart(e){ touchStartY = e.touches[0].clientY; }
  function onTouchMove(e){
    e.preventDefault();
    if(touchStartY === null) return;
    var dy = touchStartY - e.touches[0].clientY; // positive = finger moved up = scrolling forward
    if(Math.abs(dy) > 8){
      var units = Math.max(2, Math.min(MAX_EVENT_UNITS, Math.abs(dy) / 2));
      if(dy > 0) advance(units); else reverse(units);
      touchStartY = e.touches[0].clientY;
    }
  }
  function onKey(e){
    if(['ArrowDown','PageDown',' '].indexOf(e.key) !== -1){
      e.preventDefault();
      advance(MAX_EVENT_UNITS);
    } else if(['ArrowUp','PageUp'].indexOf(e.key) !== -1){
      e.preventDefault();
      reverse(MAX_EVENT_UNITS);
    }
  }
  function onSkip(){
    lines.forEach(function(line, i){
      line.classList.remove('active');
      line.classList.add('done', 'revealed');
      renderWords(i, lineWords[i].length);
    });
    finished = true;
    unlockAndHide();
  }

  window.addEventListener('wheel', onWheel, { passive:false });
  window.addEventListener('touchstart', onTouchStart, { passive:true });
  window.addEventListener('touchmove', onTouchMove, { passive:false });
  window.addEventListener('keydown', onKey);
  if(skipBtn){ skipBtn.addEventListener('click', onSkip); }
})();