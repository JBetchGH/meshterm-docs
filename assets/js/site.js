/* meshTerm docs: menu toggles, Contents sidebars with a scroll spy. No dependencies.
   Page bodies are left exactly as written; everything here is chrome added at runtime. */
(function () {
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  function toggle(button, target, after) {
    if (!button || !target) return;
    button.addEventListener('click', function () {
      var open = target.classList.toggle('is-open');
      button.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    if (after) {
      // On phones the Contents list folds away again once a section is picked.
      target.addEventListener('click', function (e) {
        if (e.target.closest('a') && target.classList.contains('is-open')) {
          target.classList.remove('is-open');
          button.setAttribute('aria-expanded', 'false');
        }
      });
    }
  }

  // Top nav menu on narrow screens.
  toggle($('.nav__toggle'), $('#nav-links'));

  // Tailscale guide: build its Contents sidebar from the existing part headings.
  var auto = $('[data-auto-toc]');
  if (auto) {
    var list = $('ul', auto);
    $$('.doc__body .section-header').forEach(function (block, i) {
      var h = $('h2', block);
      if (!h) return;
      if (!block.id) block.id = 'section-' + (i + 1);
      var li = document.createElement('li');
      var a = document.createElement('a');
      a.href = '#' + block.id; a.textContent = h.textContent;
      li.appendChild(a); list.appendChild(li);
    });
    if (list.children.length) auto.classList.add('has-items');
    toggle($('.sidebar__toggle', auto), auto, true);
  }

  // User guide: its own Contents sidebar gets a fold-away toggle on phones,
  // labelled with the sidebar's existing title.
  var guideSide = $('.page-body > .sidebar');
  if (guideSide) {
    var title = $('.sidebar-title', guideSide);
    var ul = $('ul', guideSide);
    if (title && ul) {
      if (!ul.id) ul.id = 'sidebar-list';
      var btn = document.createElement('button');
      btn.type = 'button'; btn.className = 'sidebar__toggle';
      btn.setAttribute('aria-expanded', 'false'); btn.setAttribute('aria-controls', ul.id);
      btn.textContent = title.textContent;
      guideSide.insertBefore(btn, guideSide.firstChild);
      toggle(btn, guideSide, true);
    }
  }

  // Scroll spy: highlight the sidebar link for the section in view.
  $$('.sidebar').forEach(function (side) {
    var links = $$('a[href^="#"]', side);
    var targets = links.map(function (a) {
      return document.getElementById(decodeURIComponent(a.getAttribute('href').slice(1)));
    });
    if (!links.length) return;
    var current = -2, queued = false;
    function update() {
      queued = false;
      var y = window.innerHeight * 0.25, best = -1;
      targets.forEach(function (t, i) { if (t && t.getBoundingClientRect().top <= y) best = i; });
      if (best === current) return;
      current = best;
      links.forEach(function (l, i) {
        var on = i === best;
        l.classList.toggle('active', on);
        if (on) l.setAttribute('aria-current', 'true'); else l.removeAttribute('aria-current');
      });
    }
    window.addEventListener('scroll', function () {
      if (!queued) { queued = true; window.requestAnimationFrame(update); }
    }, { passive: true });
    update();
  });
})();
