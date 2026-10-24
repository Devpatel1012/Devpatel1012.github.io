/**
 * Dev Delvadiya — Personal Portfolio Core Interactions
 * Creative Direction: "Computational Research Journal meets Contemporary Design Studio"
 */

(function () {
  'use strict';

  // ==========================================================================
  // 1. THEME MANAGEMENT (BRIGHT MODE & DARK MODE)
  // ==========================================================================

  var THEME_KEY = 'dev_portfolio_theme';
  var THEMES = ['bright', 'dark'];

  function getSystemTheme() {
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
      ? 'dark'
      : 'bright';
  }

  function getStoredTheme() {
    var stored = localStorage.getItem(THEME_KEY);
    if (stored === 'light') return 'bright'; // Seamless legacy migration
    return THEMES.indexOf(stored) !== -1 ? stored : null;
  }

  function applyTheme(theme) {
    if (THEMES.indexOf(theme) === -1) theme = 'bright';
    document.documentElement.setAttribute('data-theme', theme);

    // Update segmented theme switch buttons (Desktop & Mobile Drawer)
    var setBtns = document.querySelectorAll('[data-theme-set]');
    setBtns.forEach(function (btn) {
      var target = btn.getAttribute('data-theme-set');
      if (target === theme) {
        btn.classList.add('active');
        btn.setAttribute('aria-pressed', 'true');
      } else {
        btn.classList.remove('active');
        btn.setAttribute('aria-pressed', 'false');
      }
    });

    // Update compact mobile header toggle buttons
    var toggleBtns = document.querySelectorAll('[data-theme-toggle]');
    toggleBtns.forEach(function (btn) {
      if (theme === 'bright') {
        btn.innerHTML = '<span class="theme-icon" aria-hidden="true">🌙</span> <span class="theme-label">Dark Mode</span>';
        btn.setAttribute('aria-label', 'Theme is Bright Mode. Click to switch to Dark Mode');
        btn.setAttribute('title', 'Switch to Dark Mode');
      } else {
        btn.innerHTML = '<span class="theme-icon" aria-hidden="true">☀️</span> <span class="theme-label">Bright Mode</span>';
        btn.setAttribute('aria-label', 'Theme is Dark Mode. Click to switch to Bright Mode');
        btn.setAttribute('title', 'Switch to Bright Mode');
      }
    });
  }

  function setTheme(theme) {
    if (THEMES.indexOf(theme) === -1) theme = 'bright';
    localStorage.setItem(THEME_KEY, theme);
    applyTheme(theme);
  }

  function toggleTheme() {
    var current = document.documentElement.getAttribute('data-theme') || getStoredTheme() || getSystemTheme();
    var next = current === 'dark' ? 'bright' : 'dark';
    setTheme(next);
  }

  // Initialize immediately upon script execution
  var activeTheme = getStoredTheme() || getSystemTheme();
  applyTheme(activeTheme);

  // Synchronize theme across multiple browser tabs in real time
  window.addEventListener('storage', function (e) {
    if (e.key === THEME_KEY && e.newValue) {
      applyTheme(e.newValue);
    }
  });

  // Listen to OS theme changes if user hasn't explicitly set a preference
  if (window.matchMedia) {
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function (e) {
      if (!localStorage.getItem(THEME_KEY)) {
        applyTheme(e.matches ? 'dark' : 'bright');
      }
    });
  }

  // ==========================================================================
  // 2. MOBILE NAVIGATION DRAWER
  // ==========================================================================

  function initMobileNav() {
    var toggleBtn = document.querySelector('.mobile-toggle');
    var drawer = document.querySelector('.mobile-nav-drawer');
    if (!toggleBtn || !drawer) return;

    function openDrawer() {
      drawer.classList.add('open');
      toggleBtn.setAttribute('aria-expanded', 'true');
      toggleBtn.innerHTML = '✕';
      document.body.style.overflow = 'hidden';
    }

    function closeDrawer() {
      drawer.classList.remove('open');
      toggleBtn.setAttribute('aria-expanded', 'false');
      toggleBtn.innerHTML = '☰';
      document.body.style.overflow = '';
    }

    toggleBtn.addEventListener('click', function () {
      if (drawer.classList.contains('open')) {
        closeDrawer();
      } else {
        openDrawer();
      }
    });

    // Close on link click
    drawer.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', closeDrawer);
    });

    // Close on Escape key
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && drawer.classList.contains('open')) {
        closeDrawer();
      }
    });

    // Mobile drawer theme buttons
    drawer.querySelectorAll('[data-theme-set]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var target = btn.getAttribute('data-theme-set');
        setTheme(target);
      });
    });
  }

  // ==========================================================================
  // 3. PROJECT CATEGORY FILTERING (FOR PROJECTS.HTML)
  // ==========================================================================

  function initProjectFilters() {
    var filterBtns = document.querySelectorAll('.filter-btn');
    var projectCards = document.querySelectorAll('.project-card[data-category]');
    if (!filterBtns.length || !projectCards.length) return;

    filterBtns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var selected = btn.getAttribute('data-filter');

        filterBtns.forEach(function (b) {
          b.classList.remove('active');
          b.setAttribute('aria-pressed', 'false');
        });
        btn.classList.add('active');
        btn.setAttribute('aria-pressed', 'true');

        projectCards.forEach(function (card) {
          var cats = card.getAttribute('data-category').split(' ');
          if (selected === 'all' || cats.indexOf(selected) !== -1) {
            card.style.display = 'block';
            card.classList.add('visible');
          } else {
            card.style.display = 'none';
          }
        });
      });
    });
  }

  // ==========================================================================
  // 4. SIGNATURE COMPUTATIONAL ARTIFACT (HERO VISUALIZATION)
  // "Spatial Patch Extraction & Latent Representation Matrix"
  // ==========================================================================

  function initHeroVisualizer() {
    var canvas = document.getElementById('hero-canvas');
    if (!canvas) return;

    var ctx = canvas.getContext('2d');
    if (!ctx) return;

    var reducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    var dpr = window.devicePixelRatio || 1;
    var width = 0;
    var height = 0;

    function resize() {
      var rect = canvas.getBoundingClientRect();
      width = rect.width;
      height = rect.height;
      canvas.width = width * dpr;
      canvas.height = height * dpr;
      ctx.scale(dpr, dpr);
    }
    resize();
    window.addEventListener('resize', resize);

    // Grid of patch nodes (4x4)
    var nodes = [];
    var gridSize = 4;
    for (var r = 0; r < gridSize; r++) {
      for (var c = 0; c < gridSize; c++) {
        nodes.push({
          gridR: r,
          gridC: c,
          baseX: 0,
          baseY: 0,
          x: 0,
          y: 0,
          phase: Math.random() * Math.PI * 2,
          latentX: 0,
          latentY: 0
        });
      }
    }

    var mouse = { x: -1000, y: -1000, active: false };
    canvas.addEventListener('mousemove', function (e) {
      var rect = canvas.getBoundingClientRect();
      mouse.x = e.clientX - rect.left;
      mouse.y = e.clientY - rect.top;
      mouse.active = true;
    });
    canvas.addEventListener('mouseleave', function () {
      mouse.active = false;
    });

    var t = 0;
    function render() {
      ctx.clearRect(0, 0, width, height);

      var currentTheme = document.documentElement.getAttribute('data-theme') || 'bright';
      var isDark = currentTheme === 'dark';
      var isBright = currentTheme === 'bright';

      var primaryColor = isDark ? '#6385FF' : isBright ? '#2563EB' : '#3457D5';
      var greenColor = isDark ? '#679E7E' : isBright ? '#059669' : '#3F6E54';
      var gridLineColor = isDark
        ? 'rgba(255, 255, 255, 0.08)'
        : isBright
        ? 'rgba(15, 23, 42, 0.06)'
        : 'rgba(23, 26, 25, 0.07)';
      var projectionLineColor = isDark
        ? 'rgba(99, 133, 255, 0.16)'
        : isBright
        ? 'rgba(37, 99, 235, 0.15)'
        : 'rgba(52, 87, 213, 0.14)';
      var textColor = isDark ? '#8A908B' : isBright ? '#64748B' : '#7A807B';

      // Left zone: 2D Spatial Patch Grid
      var leftCenter = { x: width * 0.28, y: height * 0.5 };
      var patchSpacing = Math.min(width * 0.08, height * 0.2);

      // Right zone: High-dimensional Latent Embedding Space
      var rightCenter = { x: width * 0.74, y: height * 0.5 };
      var latentRadius = Math.min(width * 0.16, height * 0.36);

      // Draw subtle background coordinate ticks & boundary
      ctx.strokeStyle = gridLineColor;
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.arc(rightCenter.x, rightCenter.y, latentRadius, 0, Math.PI * 2);
      ctx.stroke();

      // Axis lines in latent space
      ctx.beginPath();
      ctx.moveTo(rightCenter.x - latentRadius - 8, rightCenter.y);
      ctx.lineTo(rightCenter.x + latentRadius + 8, rightCenter.y);
      ctx.moveTo(rightCenter.x, rightCenter.y - latentRadius - 8);
      ctx.lineTo(rightCenter.x, rightCenter.y + latentRadius + 8);
      ctx.stroke();

      // Labels
      ctx.font = '10px "JetBrains Mono", monospace';
      ctx.fillStyle = textColor;
      ctx.textAlign = 'center';
      ctx.fillText('SPATIAL PATCHES (x_p)', leftCenter.x, height - 12);
      ctx.fillText('LATENT SPACE z ∈ ℝ^d', rightCenter.x, height - 12);

      // Update and draw nodes
      nodes.forEach(function (node, i) {
        var sx = leftCenter.x + (node.gridC - (gridSize - 1) / 2) * patchSpacing;
        var sy = leftCenter.y + (node.gridR - (gridSize - 1) / 2) * patchSpacing;

        var driftX = reducedMotion ? 0 : Math.cos(t * 0.03 + node.phase) * 2;
        var driftY = reducedMotion ? 0 : Math.sin(t * 0.03 + node.phase) * 2;

        node.x = sx + driftX;
        node.y = sy + driftY;

        var angle = (i / nodes.length) * Math.PI * 2 + (reducedMotion ? 0 : t * 0.015);
        var rad = latentRadius * (0.45 + 0.45 * Math.sin(node.phase + (reducedMotion ? 0 : t * 0.02)));
        node.latentX = rightCenter.x + Math.cos(angle) * rad;
        node.latentY = rightCenter.y + Math.sin(angle) * rad;

        if (mouse.active) {
          var dx = mouse.x - node.x;
          var dy = mouse.y - node.y;
          var dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < 60) {
            node.x -= (dx / dist) * (60 - dist) * 0.15;
            node.y -= (dy / dist) * (60 - dist) * 0.15;
          }
        }

        // Draw projection line connecting Spatial Patch -> Latent Embedding
        ctx.strokeStyle = projectionLineColor;
        ctx.lineWidth = 1;
        ctx.setLineDash([3, 4]);
        ctx.beginPath();
        ctx.moveTo(node.x, node.y);
        ctx.lineTo(node.latentX, node.latentY);
        ctx.stroke();
        ctx.setLineDash([]);

        // Draw Spatial Patch node
        ctx.fillStyle = primaryColor;
        ctx.beginPath();
        ctx.arc(node.x, node.y, 3, 0, Math.PI * 2);
        ctx.fill();

        // Draw Latent Embedding vector point
        ctx.fillStyle = greenColor;
        ctx.beginPath();
        ctx.arc(node.latentX, node.latentY, 2.5, 0, Math.PI * 2);
        ctx.fill();
      });

      // Connect spatial neighbors with subtle lines
      ctx.strokeStyle = isDark
        ? 'rgba(255, 255, 255, 0.12)'
        : isBright
        ? 'rgba(15, 23, 42, 0.1)'
        : 'rgba(23, 26, 25, 0.1)';
      ctx.lineWidth = 1;
      for (var r = 0; r < gridSize; r++) {
        for (var c = 0; c < gridSize; c++) {
          var idx = r * gridSize + c;
          if (c < gridSize - 1) {
            var rightNode = idx + 1;
            ctx.beginPath();
            ctx.moveTo(nodes[idx].x, nodes[idx].y);
            ctx.lineTo(nodes[rightNode].x, nodes[rightNode].y);
            ctx.stroke();
          }
          if (r < gridSize - 1) {
            var bottomNode = idx + gridSize;
            ctx.beginPath();
            ctx.moveTo(nodes[idx].x, nodes[idx].y);
            ctx.lineTo(nodes[bottomNode].x, nodes[bottomNode].y);
            ctx.stroke();
          }
        }
      }

      t += 1;
      if (!reducedMotion) {
        requestAnimationFrame(render);
      }
    }

    render();
  }

  // ==========================================================================
  // 5. SCROLL REVEAL ANIMATIONS (INTERSECTION OBSERVER)
  // ==========================================================================

  function initScrollReveal() {
    var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var targets = document.querySelectorAll(
      '.spotlight-card, .project-card, .research-entry-card, .philosophy-card, .book-row, .art-card, .edu-card, .pub-feature-card, .pub-item, .stack-box, .collab-banner, .cred-strip'
    );

    if (!targets.length) return;

    if (reduced || !('IntersectionObserver' in window)) {
      targets.forEach(function (el) {
        el.classList.add('visible');
      });
      return;
    }

    targets.forEach(function (el) {
      el.classList.add('reveal');
    });

    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.05, rootMargin: '0px 0px 40px 0px' }
    );

    targets.forEach(function (el) {
      io.observe(el);
    });
  }

  // ==========================================================================
  // 6. ACADEMIC DATA LOADERS & INTERACTIONS
  // ==========================================================================

  function showToast(msg) {
    var toast = document.querySelector('.toast-feedback');
    if (!toast) {
      toast = document.createElement('div');
      toast.className = 'toast-feedback';
      document.body.appendChild(toast);
    }
    toast.textContent = msg;
    toast.classList.add('show');
    clearTimeout(toast._timeout);
    toast._timeout = setTimeout(function () {
      toast.classList.remove('show');
    }, 2600);
  }

  function initAcademicInteractions() {
    // BibTeX toggles and copy
    document.addEventListener('click', function (e) {
      var toggleBtn = e.target.closest('[data-bibtex-toggle]');
      if (toggleBtn) {
        e.preventDefault();
        var targetId = toggleBtn.getAttribute('data-bibtex-toggle');
        var targetBox = document.getElementById(targetId);
        if (targetBox) {
          targetBox.classList.toggle('open');
        }
        return;
      }

      var copyBtn = e.target.closest('[data-bibtex-copy]');
      if (copyBtn) {
        e.preventDefault();
        var targetId = copyBtn.getAttribute('data-bibtex-copy');
        var codeEl = document.getElementById(targetId);
        if (codeEl) {
          var text = codeEl.textContent.trim();
          navigator.clipboard.writeText(text).then(function () {
            showToast('BibTeX citation copied to clipboard!');
          }).catch(function () {
            showToast('Failed to copy. Please select and copy manually.');
          });
        }
        return;
      }

      var cmdCopy = e.target.closest('.copy-cmd-btn');
      if (cmdCopy) {
        e.preventDefault();
        var terminal = cmdCopy.closest('.reproduce-terminal');
        if (terminal) {
          var clone = terminal.cloneNode(true);
          var btn = clone.querySelector('.copy-cmd-btn');
          if (btn) btn.remove();
          var cmdText = clone.textContent.trim();
          navigator.clipboard.writeText(cmdText).then(function () {
            showToast('Command copied to clipboard!');
          });
        }
        return;
      }
    });
  }

  // Optional dynamic data hydration from JSON files (with progressive enhancement)
  function initDynamicDataLoaders() {
    if (window.location.protocol.indexOf('http') !== 0) {
      // Local file:// protocol has browser security restrictions on fetch().
      // The static semantic HTML fallback is already rendered and complete.
      return;
    }

    var newsContainer = document.querySelector('[data-render="news"]');
    if (newsContainer) {
      fetch('data/news.json')
        .then(function (res) { return res.ok ? res.json() : null; })
        .then(function (items) {
          if (!items || !items.length) return;
          var html = items.map(function (item) {
            var badgeClass = item.badge.toLowerCase();
            return '<li class="news-item">' +
              '<span class="news-date mono">' + item.date + '</span>' +
              '<span class="news-badge ' + badgeClass + '">' + item.badge + '</span>' +
              '<span class="news-text">' + item.text + '</span>' +
              '</li>';
          }).join('');
          newsContainer.innerHTML = html;
        })
        .catch(function () {
          // Keep static HTML fallback intact
        });
    }

    var readingContainer = document.querySelector('[data-render="reading"]');
    if (readingContainer) {
      fetch('data/reading.json')
        .then(function (res) { return res.ok ? res.json() : null; })
        .then(function (books) {
          if (!books || !books.length) return;
          var html = books.map(function (b) {
            var statusClass = b.status.toLowerCase().indexOf('active') !== -1 || b.status.toLowerCase().indexOf('reading') !== -1 ? 'reading' : 'completed';
            return '<div class="book-row">' +
              '<span class="book-callno mono">' + b.id + '</span>' +
              '<div class="book-info">' +
              '<span class="book-title">' + b.title + '</span>' +
              '<span class="book-author">' + b.author + '</span>' +
              '<span class="book-takeaway"><strong>Why it mattered:</strong> ' + b.relevance + '</span>' +
              '</div>' +
              '<span class="book-status ' + statusClass + '">' + b.status + '</span>' +
              '</div>';
          }).join('');
          readingContainer.innerHTML = html;
        })
        .catch(function () {
          // Keep static HTML fallback intact
        });
    }
  }

  // ==========================================================================
  // INITIALIZATION ON DOM READY
  // ==========================================================================

  document.addEventListener('DOMContentLoaded', function () {
    // Theme switch buttons (explicit mode selection: Bright Mode / Dark Mode)
    document.querySelectorAll('[data-theme-set]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var target = btn.getAttribute('data-theme-set');
        setTheme(target);
      });
    });

    // Mobile compact toggle buttons (binary toggle between Bright Mode and Dark Mode)
    document.querySelectorAll('[data-theme-toggle]').forEach(function (btn) {
      btn.addEventListener('click', toggleTheme);
    });

    // Ensure active state on initial load
    var current = document.documentElement.getAttribute('data-theme') || getStoredTheme() || getSystemTheme();
    applyTheme(current);

    initMobileNav();
    initProjectFilters();
    initHeroVisualizer();
    initScrollReveal();
    initAcademicInteractions();
    initDynamicDataLoaders();
  });
})();
