/* Domaine du Geisberg — scripts communs : menu, thème, diaporama d'accueil, galerie, calendrier, mode notes. */
(function () {
  'use strict';
  var root = document.documentElement;
  root.classList.add('js');
  var reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Thème clair / sombre (mémorisé) */
  try {
    var th = localStorage.getItem('geisberg-theme');
    if (th === 'dark' || th === 'light') root.setAttribute('data-theme', th);
  } catch (e) {}
  var tbtn = document.getElementById('theme');
  if (tbtn)
    tbtn.addEventListener('click', function () {
      var v = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', v);
      try {
        localStorage.setItem('geisberg-theme', v);
      } catch (e) {}
    });

  /* Menu mobile */
  var mbtn = document.getElementById('menu'),
    nav = document.getElementById('nav'),
    bd = document.getElementById('backdrop'),
    xbtn = document.getElementById('menu-close');
  if (mbtn && nav) {
    function setMenu(o) {
      nav.classList.toggle('open', o);
      mbtn.setAttribute('aria-expanded', o);
      if (bd) bd.hidden = !o;
      document.body.classList.toggle('menu-open', o);
      if (o) {
        var f = nav.querySelector('a');
        f && f.focus();
      }
    }
    mbtn.addEventListener('click', function () {
      setMenu(!nav.classList.contains('open'));
    });
    xbtn &&
      xbtn.addEventListener('click', function () {
        setMenu(false);
        mbtn.focus();
      });
    bd &&
      bd.addEventListener('click', function () {
        setMenu(false);
      });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a') && window.innerWidth < 1040) setMenu(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('open')) {
        setMenu(false);
        mbtn.focus();
      }
    });
    matchMedia('(min-width: 1040px)').addEventListener('change', function (m) {
      if (m.matches) setMenu(false);
    });
  }

  /* Menu déroulant des langues (ordinateur) : se referme quand on clique ailleurs ou avec Échap */
  var langdd = document.querySelector('.langdd');
  if (langdd) {
    document.addEventListener('click', function (e) {
      if (langdd.open && !langdd.contains(e.target)) langdd.open = false;
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && langdd.open) langdd.open = false;
    });
  }

  /* Diaporama d'accueil (fondu toutes les 5 s) */
  var hero = document.querySelector('.hero');
  if (hero) {
    var slides = hero.querySelectorAll('.slide'),
      dots = hero.querySelectorAll('.dots button'),
      cur = 0,
      timer;
    function go(i) {
      slides[cur].classList.remove('on');
      dots[cur] && dots[cur].removeAttribute('aria-current');
      cur = (i + slides.length) % slides.length;
      slides[cur].classList.add('on');
      dots[cur] && dots[cur].setAttribute('aria-current', 'true');
    }
    function start() {
      clearInterval(timer);
      if (!matchMedia('(prefers-reduced-motion: reduce)').matches)
        timer = setInterval(function () {
          go(cur + 1);
        }, 7000);
    }
    dots.forEach(function (d, i) {
      d.addEventListener('click', function () {
        go(i);
        start();
      });
    });
    if (slides.length > 1) start();
  }

  /* Galerie → visionneuse */
  var links = Array.prototype.slice.call(document.querySelectorAll('.gallery a, .mosaic a'));
  if (links.length) {
    var lb = document.createElement('figure');
    lb.className = 'lb';
    lb.setAttribute('role', 'dialog');
    lb.setAttribute('aria-modal', 'true');
    var L = window.GEISBERG_UI || {};
    lb.innerHTML =
      '<img alt=""><figcaption></figcaption><button class="x" aria-label="' +
      (L.close || 'Fermer') +
      '">×</button><button class="p" aria-label="' +
      (L.prev || 'Précédent') +
      '">‹</button><button class="n" aria-label="' +
      (L.next || 'Suivant') +
      '">›</button>';
    document.body.appendChild(lb);
    var li = 0,
      img = lb.querySelector('img'),
      cap = lb.querySelector('figcaption');
    function show(i) {
      li = (i + links.length) % links.length;
      img.src = links[li].getAttribute('href');
      var a = links[li].querySelector('img');
      img.alt = a ? a.alt : '';
      cap.textContent = links[li].getAttribute('data-cap') || (a ? a.alt : '');
    }
    function open(i) {
      show(i);
      lb.classList.add('open');
      document.body.style.overflow = 'hidden';
      lb.querySelector('.x').focus();
    }
    function close() {
      lb.classList.remove('open');
      document.body.style.overflow = '';
    }
    links.forEach(function (a, i) {
      a.addEventListener('click', function (e) {
        e.preventDefault();
        open(i);
      });
    });
    lb.querySelector('.x').addEventListener('click', close);
    lb.querySelector('.p').addEventListener('click', function () {
      show(li - 1);
    });
    lb.querySelector('.n').addEventListener('click', function () {
      show(li + 1);
    });
    lb.addEventListener('click', function (e) {
      if (e.target === lb) close();
    });
    document.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') show(li - 1);
      if (e.key === 'ArrowRight') show(li + 1);
    });
    var sx = 0;
    lb.addEventListener(
      'touchstart',
      function (e) {
        sx = e.touches[0].clientX;
      },
      { passive: true },
    );
    lb.addEventListener('touchend', function (e) {
      var dx = e.changedTouches[0].clientX - sx;
      if (Math.abs(dx) > 50) show(li + (dx < 0 ? 1 : -1));
    });
  }

  /* Mode « Notes pour Marc » : inactif tant qu'on n'appuie pas sur le bouton (ou #notes). */
  var nbtn = document.getElementById('nbtn'),
    items = Array.prototype.slice.call(document.querySelectorAll('[data-note]'));
  if (nbtn) {
    var list = document.getElementById('nlist');
    if (!items.length) {
      list.innerHTML = '<li>Rien à fournir sur cette page.</li>';
    }
    items.forEach(function (el, i) {
      var n = i + 1,
        b = document.createElement('button');
      b.type = 'button';
      b.className = 'nbub';
      b.textContent = n;
      b.setAttribute('aria-label', 'Note ' + n);
      var t = document.createElement('div');
      t.className = 'ntip';
      t.innerHTML = '<b>Note ' + n + '</b>';
      t.appendChild(document.createTextNode(el.getAttribute('data-note')));
      b.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        var o = el.classList.contains('open');
        items.forEach(function (x) {
          x.classList.remove('open');
        });
        if (!o) el.classList.add('open');
      });
      el.appendChild(b);
      el.appendChild(t);
      var li = document.createElement('li'),
        num = document.createElement('i'),
        sp = document.createElement('span');
      num.textContent = n;
      sp.textContent = el.getAttribute('data-note');
      li.appendChild(num);
      li.appendChild(sp);
      list.appendChild(li);
    });
    function set(on) {
      root.classList.toggle('notes', on);
      nbtn.setAttribute('aria-pressed', on);
      nbtn.querySelector('span').textContent = on
        ? nbtn.getAttribute('data-hide')
        : nbtn.getAttribute('data-show');
      if (!on)
        items.forEach(function (x) {
          x.classList.remove('open');
        });
    }
    nbtn.addEventListener('click', function () {
      set(!root.classList.contains('notes'));
    });
    if (location.hash === '#notes') set(true);
  }

  /* ---------- Effets discrets ---------- */

  /* Apparition progressive des blocs à l'entrée dans l'écran, avec un léger décalage entre voisins */
  var revealSel =
    '.sec-head, .fact, .card, .tile, .mosaic > *, .gallery > *, .reviews > *, .hosts, .diapo-teaser, ' +
    '.strip > *, .logos > *, .cols > *, .prices, .ratings > *, .chips > *, .list > li, .visite, .dispo, ' +
    '.domaine-band, .videos > *, .links-row, .cal-row > *';
  var toReveal = Array.prototype.slice.call(document.querySelectorAll(revealSel));
  if (toReveal.length && 'IntersectionObserver' in window && !reduced) {
    toReveal.forEach(function (el) {
      var i = Array.prototype.indexOf.call(el.parentNode.children, el);
      el.classList.add('reveal');
      el.style.setProperty('--d', Math.min(i, 6) * 0.08 + 's');
    });
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) {
            en.target.classList.add('in');
            io.unobserve(en.target);
          }
        });
      },
      { rootMargin: '0px 0px -8% 0px', threshold: 0.08 }
    );
    toReveal.forEach(function (el) {
      io.observe(el);
    });
  }

  /* Fondu des photos chargées à la demande */
  Array.prototype.forEach.call(document.querySelectorAll('img[loading="lazy"]'), function (img) {
    if (img.complete || reduced) return;
    if (img.closest('.diapo') || img.closest('.hero')) return; // ces images ont déjà leur propre fondu
    img.classList.add('fade');
    img.addEventListener(
      'load',
      function () {
        img.classList.add('ld');
      },
      { once: true }
    );
    img.addEventListener(
      'error',
      function () {
        img.classList.add('ld');
      },
      { once: true }
    );
  });

  /* Ombre de l'en-tête et bouton « remonter » selon le défilement */
  var header = document.querySelector('.site-header'),
    totop = document.createElement('button');
  totop.type = 'button';
  totop.className = 'totop';
  totop.setAttribute('aria-label', (window.GEISBERG_UI && GEISBERG_UI.top) || 'Haut de page');
  totop.innerHTML =
    '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7"/></svg>';
  totop.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: reduced ? 'auto' : 'smooth' });
  });
  document.body.appendChild(totop);
  var ticking = false;
  function onScroll() {
    var y = window.scrollY || document.documentElement.scrollTop;
    header && header.classList.toggle('scrolled', y > 8);
    totop.classList.toggle('show', y > 700);
    ticking = false;
  }
  window.addEventListener(
    'scroll',
    function () {
      if (!ticking) {
        ticking = true;
        requestAnimationFrame(onScroll);
      }
    },
    { passive: true }
  );
  onScroll();
})();
