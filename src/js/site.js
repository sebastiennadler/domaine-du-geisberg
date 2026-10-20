/* Domaine du Geisberg — scripts communs : menu, thème, diaporama d'accueil, galerie, calendriers Nuitrésa, mode notes. */
(function () {
  'use strict';
  var root = document.documentElement;
  root.classList.add('js');
  var reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  /* Textes de l'interface (Fermer, Précédent…) : bloc JSON écrit par base.html, pas de script en ligne (CSP). */
  var UI = {};
  try {
    var uiEl = document.getElementById('ui-strings');
    if (uiEl) UI = JSON.parse(uiEl.textContent) || {};
  } catch (e) {}

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

  /* Bandeau d'accueil : la photo des hôtes reste fixe (data-dur, ~4 s), puis chaque photo part de loin et zoome
     en glissant (animation CSS, durée --dur = durée de la photo + fondu). Inclinaison à la souris (data-tilt) et
     parallaxe au défilement (data-parallax) sur le calque des photos : interrupteurs dans shared.json. */
  var hero = document.querySelector('.hero');
  if (hero) {
    var slides = hero.querySelectorAll('.slide'),
      dots = hero.querySelectorAll('.dots button'),
      layer = hero.querySelector('.layer'),
      cur = 0,
      timer,
      reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
    slides.forEach(function (sl) {
      sl.style.setProperty('--dur', (parseInt(sl.getAttribute('data-dur'), 10) || 7000) + 1800 + 'ms');
    });
    function go(i) {
      var next = (i + slides.length) % slides.length,
        img = slides[next].querySelector('img');
      /* on attend que la photo suivante soit décodée : jamais de fondu vers une photo pas encore chargée */
      var ready = img && img.decode ? img.decode().catch(function () {}) : Promise.resolve();
      var done = false;
      function swap() {
        if (done) return;
        done = true;
        slides[cur].classList.remove('on');
        dots[cur] && dots[cur].removeAttribute('aria-current');
        cur = next;
        if (img) {
          /* relance l'animation « de loin vers le près » à chaque passage */
          img.style.animation = 'none';
          void img.offsetWidth;
          img.style.animation = '';
        }
        slides[cur].classList.add('on');
        dots[cur] && dots[cur].setAttribute('aria-current', 'true');
        start();
      }
      ready.then(swap);
      setTimeout(swap, 2500);
    }
    function start() {
      clearTimeout(timer);
      if (!reduced && slides.length > 1)
        timer = setTimeout(function () {
          go(cur + 1);
        }, parseInt(slides[cur].getAttribute('data-dur'), 10) || 7000);
    }
    dots.forEach(function (d, i) {
      d.addEventListener('click', function () {
        go(i);
      });
    });
    start();
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) clearTimeout(timer);
      else start();
    });

    /* Inclinaison 3D à la souris + parallaxe : un seul transform, recalculé au plus une fois par image */
    var tilt = hero.getAttribute('data-tilt') === 'on' && matchMedia('(hover: hover) and (pointer: fine)').matches,
      para = hero.getAttribute('data-parallax') === 'on',
      rx = 0,
      ry = 0,
      tx = 0,
      ty = 0,
      py = 0,
      raf = null;
    function paint() {
      raf = null;
      rx += (tx - rx) * 0.08;
      ry += (ty - ry) * 0.08;
      if (layer)
        layer.style.transform =
          'translate3d(0,' + py.toFixed(1) + 'px,0) rotateX(' + rx.toFixed(2) + 'deg) rotateY(' + ry.toFixed(2) + 'deg) scale(1.06)';
      var txt = hero.querySelector('.wrap');
      if (txt && para) txt.style.transform = 'translate3d(0,' + (py * 0.45).toFixed(1) + 'px,0)';
      if (Math.abs(tx - rx) > 0.02 || Math.abs(ty - ry) > 0.02) raf = requestAnimationFrame(paint);
    }
    function ask() {
      if (!raf) raf = requestAnimationFrame(paint);
    }
    if (!reduced && (tilt || para)) {
      if (tilt) {
        hero.addEventListener('mousemove', function (e) {
          var r = hero.getBoundingClientRect();
          ty = ((e.clientX - r.left) / r.width - 0.5) * 5; /* ±2,5° */
          tx = -((e.clientY - r.top) / r.height - 0.5) * 3.5;
          ask();
        });
        hero.addEventListener('mouseleave', function () {
          tx = ty = 0;
          ask();
        });
      }
      if (para) {
        var onScroll = function () {
          var y = window.scrollY || 0;
          py = Math.min(y, hero.offsetHeight) * 0.25;
          ask();
        };
        window.addEventListener('scroll', onScroll, { passive: true });
        onScroll();
      }
    }

    /* Bouton « Diaporama » : ouvre le diaporama complet en superposition, photos chargées à ce moment-là */
    var openBtn = document.getElementById('open-diapo'),
      overlay = document.getElementById('home-diapo');
    if (openBtn && overlay) {
      openBtn.addEventListener('click', function () {
        overlay.querySelectorAll('img[data-src]').forEach(function (im) {
          im.src = im.getAttribute('data-src');
          im.removeAttribute('data-src');
        });
        overlay.hidden = false;
        document.body.style.overflow = 'hidden';
        clearTimeout(timer);
        var app = overlay.querySelector('.diapo-app');
        if (app && app.geisbergDiapo) app.geisbergDiapo.open();
      });
    }
  }

  /* Diaporama (page En images et superposition de l'accueil) : fondu toutes les 5 s, pause, plein écran,
     chants d'oiseaux, clavier et gestes. Un composant par élément .diapo-app. */
  window.geisbergDiapos = [];
  Array.prototype.slice.call(document.querySelectorAll('.diapo-app')).forEach(function (app) {
    var box = app.querySelector('.diapo'),
      imgs = box.querySelectorAll('img'),
      g = box.querySelector('b[data-group]'),
      c = box.querySelector('span[data-cap]'),
      ix = box.querySelector('[data-idx]'),
      play = app.querySelector('.diapo-ctl [data-play]'),
      au = app.querySelector('audio'),
      ab = app.querySelector('[data-audio]'),
      overlayBox = app.closest('.diapo-overlay'),
      i = 0,
      t,
      on = true;
    function show(n) {
      imgs[i].classList.remove('on');
      i = (n + imgs.length) % imgs.length;
      imgs[i].classList.add('on');
      g.textContent = imgs[i].getAttribute('data-group');
      c.textContent = imgs[i].getAttribute('data-cap');
      ix.textContent = i + 1 + ' / ' + imgs.length;
    }
    function run() {
      clearInterval(t);
      if (on)
        t = setInterval(function () {
          show(i + 1);
        }, 5000);
    }
    function setPlay(v) {
      on = v;
      play.setAttribute('aria-pressed', on);
      play.classList.toggle('paused', !on);
      play.setAttribute('aria-label', on ? app.getAttribute('data-label-pause') : app.getAttribute('data-label-play'));
      run();
    }
    function setAudio(v) {
      ab.setAttribute('aria-pressed', v);
      ab.classList.toggle('on', v);
      ab.querySelector('span').textContent = v ? ab.getAttribute('data-off') : ab.getAttribute('data-on');
      ab.setAttribute('aria-label', ab.querySelector('span').textContent);
      if (v) {
        au.volume = 0.6;
        au.play().catch(function () {
          setAudio(false);
        });
      } else au.pause();
      try {
        localStorage.setItem('geisberg-birds', v ? '1' : '0');
      } catch (e) {}
    }
    function fsOn() {
      return document.fullscreenElement === box || box.classList.contains('fs');
    }
    function enter() {
      if (box.requestFullscreen && !/iPhone|iPad|iPod/.test(navigator.userAgent)) {
        box.requestFullscreen().catch(function () {
          box.classList.add('fs');
          document.body.style.overflow = 'hidden';
        });
      } else {
        box.classList.add('fs');
        document.body.style.overflow = 'hidden';
      }
    }
    function exit() {
      if (document.fullscreenElement) document.exitFullscreen().catch(function () {});
      box.classList.remove('fs');
      if (!overlayBox || overlayBox.hidden) document.body.style.overflow = '';
    }
    function close() {
      exit();
      setPlay(false);
      if (ab.getAttribute('aria-pressed') === 'true') setAudio(false);
      if (overlayBox) {
        overlayBox.hidden = true;
        document.body.style.overflow = '';
      }
    }
    app.querySelectorAll('[data-prev]').forEach(function (b) {
      b.onclick = function (e) {
        e.stopPropagation();
        show(i - 1);
        run();
      };
    });
    app.querySelectorAll('[data-next]').forEach(function (b) {
      b.onclick = function (e) {
        e.stopPropagation();
        show(i + 1);
        run();
      };
    });
    play.onclick = function () {
      setPlay(!on);
    };
    ab.onclick = function () {
      setAudio(ab.getAttribute('aria-pressed') !== 'true');
    };
    try {
      if (localStorage.getItem('geisberg-birds') === '1') ab.classList.add('hint');
    } catch (e) {}
    app.querySelector('[data-full]').onclick = function () {
      fsOn() ? exit() : enter();
    };
    app.querySelector('[data-x]').onclick = function (e) {
      e.stopPropagation();
      overlayBox ? close() : exit();
    };
    var closeBtn = app.querySelector('[data-close]');
    if (closeBtn) closeBtn.onclick = close;
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) au.pause();
      else if (ab.getAttribute('aria-pressed') === 'true') au.play().catch(function () {});
    });
    document.addEventListener('keydown', function (e) {
      if (overlayBox && overlayBox.hidden) return;
      if (e.key === 'Escape') overlayBox ? close() : exit();
      if (box.offsetParent === null && !fsOn()) return;
      if (e.key === 'ArrowLeft') {
        show(i - 1);
        run();
      }
      if (e.key === 'ArrowRight') {
        show(i + 1);
        run();
      }
      if (e.key === ' ' && fsOn()) {
        e.preventDefault();
        play.click();
      }
    });
    box.addEventListener('click', function (e) {
      if (e.target.tagName === 'BUTTON') return;
      show(i + 1);
      run();
    });
    var sx = 0;
    box.addEventListener(
      'touchstart',
      function (e) {
        sx = e.touches[0].clientX;
      },
      { passive: true }
    );
    box.addEventListener('touchend', function (e) {
      var dx = e.changedTouches[0].clientX - sx;
      if (Math.abs(dx) > 50) {
        show(i + (dx < 0 ? 1 : -1));
        run();
      }
    });
    app.geisbergDiapo = {
      pause: function () {
        if (on) setPlay(false);
        if (ab.getAttribute('aria-pressed') === 'true') setAudio(false);
      },
      open: function () {
        show(0);
        setPlay(true);
      },
    };
    window.geisbergDiapos.push(app.geisbergDiapo);
    show(0);
    if (overlayBox) on = false;
    else run();
  });

  /* Galerie → visionneuse */
  var links = Array.prototype.slice.call(document.querySelectorAll('.gallery a, .mosaic a'));
  if (links.length) {
    var lb = document.createElement('figure');
    lb.className = 'lb';
    lb.setAttribute('role', 'dialog');
    lb.setAttribute('aria-modal', 'true');
    var L = UI;
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

  /* Calendriers Nuitrésa : le cadre envoie sa hauteur (postMessage, frameId = id du cadre) quand son contenu
     change — mois suivant, écran étroit où les deux mois s'empilent. On n'écoute que l'origine de Nuitrésa. */
  window.addEventListener('message', function (e) {
    if (e.origin !== 'https://public.nuit-resa.com') return;
    var d = e.data || {},
      h = parseInt(d.height || d.frameHeight, 10),
      f = d.frameId ? document.getElementById(d.frameId) : null;
    if (h > 0 && f && f.classList.contains('nr-cal')) f.style.height = h + 20 + 'px';
  });

  /* ---------- Onglets de la page « En images » ---------- */
  /* L'ancre choisit l'onglet (#diaporama, #videos, #visite) ; la visite 360° (cadre externe) n'est chargée qu'à l'ouverture
     de son onglet ; les diaporamas se mettent en pause quand on quitte le leur. */
  var tabs = Array.prototype.slice.call(document.querySelectorAll('.tabs [role=tab]')),
    panels = Array.prototype.slice.call(document.querySelectorAll('.panel[role=tabpanel]'));
  if (tabs.length && panels.length) {
    var openTab = function (id, push) {
      if (!document.getElementById(id)) id = panels[0].id;
      tabs.forEach(function (t) {
        t.setAttribute('aria-selected', t.getAttribute('aria-controls') === id);
      });
      panels.forEach(function (p) {
        p.hidden = p.id !== id;
      });
      var f = document.querySelector('#visite iframe');
      if (id === 'visite' && f && !f.src) f.src = f.getAttribute('data-src');
      if (id !== 'diaporama' && window.geisbergDiapos)
        window.geisbergDiapos.forEach(function (d) {
          d.pause();
        });
      if (push) history.replaceState(null, '', '#' + id);
    };
    tabs.forEach(function (t) {
      t.addEventListener('click', function (e) {
        e.preventDefault();
        openTab(t.getAttribute('aria-controls'), true);
        t.focus();
      });
    });
    window.addEventListener('hashchange', function () {
      openTab(location.hash.slice(1), false);
    });
    openTab(location.hash.slice(1) || panels[0].id, false);
  }

  /* ---------- Effets discrets ---------- */

  /* Apparition progressive des blocs à l'entrée dans l'écran, avec un léger décalage entre voisins */
  var revealSel =
    '.sec-head, .fact, .card, .tile, .mosaic > *, .gallery > *, .reviews > *, .hosts, .diapo-teaser, ' +
    '.strip > *, .logos > *, .cols > *, .prices, .ratings > *, .chips > *, .list > li, .visite, .dispo, ' +
    '.videos > *, .links-row, .cal-box, .teaser, .fiche, .drawer, .incl, .tabs';
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
  totop.setAttribute('aria-label', UI.top || 'Haut de page');
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
