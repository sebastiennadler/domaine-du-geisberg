/* Domaine du Geisberg — scripts communs : menu, thème, diaporama d'accueil, galerie, calendrier, mode notes. */
(function () {
  'use strict';
  var root = document.documentElement;

  /* Thème clair / sombre (mémorisé) */
  try { var th = localStorage.getItem('geisberg-theme'); if (th === 'dark' || th === 'light') root.setAttribute('data-theme', th); } catch (e) {}
  var tbtn = document.getElementById('theme');
  if (tbtn) tbtn.addEventListener('click', function () {
    var v = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', v);
    try { localStorage.setItem('geisberg-theme', v); } catch (e) {}
  });

  /* Menu mobile */
  var mbtn = document.getElementById('menu'), nav = document.getElementById('nav'), bd = document.getElementById('backdrop'), xbtn = document.getElementById('menu-close');
  if (mbtn && nav) {
    function setMenu(o) { nav.classList.toggle('open', o); mbtn.setAttribute('aria-expanded', o); if (bd) bd.hidden = !o; document.body.classList.toggle('menu-open', o); if (o) { var f = nav.querySelector('a'); f && f.focus(); } }
    mbtn.addEventListener('click', function () { setMenu(!nav.classList.contains('open')); });
    xbtn && xbtn.addEventListener('click', function () { setMenu(false); mbtn.focus(); });
    bd && bd.addEventListener('click', function () { setMenu(false); });
    nav.addEventListener('click', function (e) { if (e.target.closest('a') && window.innerWidth < 960) setMenu(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && nav.classList.contains('open')) { setMenu(false); mbtn.focus(); } });
    matchMedia('(min-width: 960px)').addEventListener('change', function (m) { if (m.matches) setMenu(false); });
  }

  /* Diaporama d'accueil (fondu toutes les 5 s) */
  var hero = document.querySelector('.hero');
  if (hero) {
    var slides = hero.querySelectorAll('.slide'), dots = hero.querySelectorAll('.dots button'), cur = 0, timer;
    function go(i) {
      slides[cur].classList.remove('on'); dots[cur] && dots[cur].removeAttribute('aria-current');
      cur = (i + slides.length) % slides.length;
      slides[cur].classList.add('on'); dots[cur] && dots[cur].setAttribute('aria-current', 'true');
    }
    function start() { clearInterval(timer); if (!matchMedia('(prefers-reduced-motion: reduce)').matches) timer = setInterval(function () { go(cur + 1); }, 5000); }
    dots.forEach(function (d, i) { d.addEventListener('click', function () { go(i); start(); }); });
    if (slides.length > 1) start();
  }

  /* Galerie → visionneuse */
  var links = Array.prototype.slice.call(document.querySelectorAll('.gallery a, .mosaic a'));
  if (links.length) {
    var lb = document.createElement('figure'); lb.className = 'lb'; lb.setAttribute('role', 'dialog'); lb.setAttribute('aria-modal', 'true');
    var L = window.GEISBERG_UI || {};
    lb.innerHTML = '<img alt=""><figcaption></figcaption><button class="x" aria-label="' + (L.close || 'Fermer') + '">×</button><button class="p" aria-label="' + (L.prev || 'Précédent') + '">‹</button><button class="n" aria-label="' + (L.next || 'Suivant') + '">›</button>';
    document.body.appendChild(lb);
    var li = 0, img = lb.querySelector('img'), cap = lb.querySelector('figcaption');
    function show(i) { li = (i + links.length) % links.length; img.src = links[li].getAttribute('href'); var a = links[li].querySelector('img'); img.alt = a ? a.alt : ''; cap.textContent = links[li].getAttribute('data-cap') || (a ? a.alt : ''); }
    function open(i) { show(i); lb.classList.add('open'); document.body.style.overflow = 'hidden'; lb.querySelector('.x').focus(); }
    function close() { lb.classList.remove('open'); document.body.style.overflow = ''; }
    links.forEach(function (a, i) { a.addEventListener('click', function (e) { e.preventDefault(); open(i); }); });
    lb.querySelector('.x').addEventListener('click', close);
    lb.querySelector('.p').addEventListener('click', function () { show(li - 1); });
    lb.querySelector('.n').addEventListener('click', function () { show(li + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
    document.addEventListener('keydown', function (e) { if (!lb.classList.contains('open')) return; if (e.key === 'Escape') close(); if (e.key === 'ArrowLeft') show(li - 1); if (e.key === 'ArrowRight') show(li + 1); });
    var sx = 0; lb.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', function (e) { var dx = e.changedTouches[0].clientX - sx; if (Math.abs(dx) > 50) show(li + (dx < 0 ? 1 : -1)); });
  }

  /* Calendrier de disponibilités : lit data-busy="AAAA-MM-JJ/AAAA-MM-JJ,..." (plus tard : flux iCal). */
  document.querySelectorAll('.cal').forEach(function (cal) {
    var lang = root.getAttribute('lang') || 'fr', busy = (cal.getAttribute('data-busy') || '').split(',').filter(Boolean).map(function (r) { var p = r.split('/'); return [new Date(p[0]), new Date(p[1])]; });
    var now = new Date(), y = now.getFullYear(), m = now.getMonth(), hd = cal.querySelector('.hd b'), g = cal.querySelector('.g');
    var days = cal.getAttribute('data-days') ? cal.getAttribute('data-days').split(',') : ['L', 'M', 'M', 'J', 'V', 'S', 'D'];
    function render() {
      var first = new Date(y, m, 1), off = (first.getDay() + 6) % 7, n = new Date(y, m + 1, 0).getDate(), h = '';
      hd.textContent = first.toLocaleDateString(lang, { month: 'long', year: 'numeric' });
      days.forEach(function (d) { h += '<i>' + d + '</i>'; });
      for (var i = 0; i < off; i++) h += '<span class="off"></span>';
      for (var d = 1; d <= n; d++) {
        var dt = new Date(y, m, d), c = '';
        if (dt < new Date(now.getFullYear(), now.getMonth(), now.getDate())) c = ' past';
        busy.forEach(function (b) { if (dt >= b[0] && dt < b[1]) c += ' busy'; });
        h += '<span class="' + c.trim() + '">' + d + '</span>';
      }
      g.innerHTML = h;
    }
    cal.querySelector('.hd .prev').addEventListener('click', function () { m--; if (m < 0) { m = 11; y--; } render(); });
    cal.querySelector('.hd .next').addEventListener('click', function () { m++; if (m > 11) { m = 0; y++; } render(); });
    render();
  });

  /* Formulaire : envoi par FormSubmit (AJAX) vers la boîte mail ; repli sur un e-mail pré-rempli si l'envoi échoue. */
  var f = document.getElementById('resa');
  if (f) f.addEventListener('submit', function (e) {
    e.preventDefault();
    var st = document.getElementById('f_status'), btn = document.getElementById('f_btn');
    var v = function (id) { var el = f.querySelector('#' + id); return el ? el.value : ''; };
    function fallback() {
      var body = [v('f_subject'), v('f_name'), v('f_email'), v('f_phone'), '', v('f_gite') + ' · ' + v('f_in') + ' → ' + v('f_out') + ' · ' + v('f_people'), '', v('f_msg')].join('\n');
      st.innerHTML = f.getAttribute('data-ko') + ' <a href="mailto:' + f.getAttribute('data-to') + '">' + f.getAttribute('data-to') + '</a>.';
      location.href = 'mailto:' + f.getAttribute('data-to') + '?subject=' + encodeURIComponent(f.getAttribute('data-subject') + ' ' + v('f_in') + ' → ' + v('f_out')) + '&body=' + encodeURIComponent(body);
    }
    btn.disabled = true; btn.textContent = f.getAttribute('data-sending');
    var fd = new FormData(f); fd.append('_replyto', v('f_email'));
    fetch(f.getAttribute('action'), { method: 'POST', body: fd, headers: { 'Accept': 'application/json' } })
      .then(function (r) { return r.ok ? r.json() : Promise.reject(); })
      .then(function () { st.textContent = f.getAttribute('data-ok'); f.reset(); btn.textContent = f.getAttribute('data-send'); btn.disabled = false; })
      .catch(function () { btn.textContent = f.getAttribute('data-send'); btn.disabled = false; fallback(); });
  });

  /* Mode « Notes pour Marc » : inactif tant qu'on n'appuie pas sur le bouton (ou #notes). */
  var nbtn = document.getElementById('nbtn'), items = Array.prototype.slice.call(document.querySelectorAll('[data-note]'));
  if (nbtn) {
    var list = document.getElementById('nlist'), done = {}; if (!items.length) { list.innerHTML = '<li>Rien à fournir sur cette page.</li>'; } try { done = JSON.parse(localStorage.getItem('notes-done') || '{}'); } catch (e) {}
    var page = location.pathname.split('/').pop() || 'index.html';
    items.forEach(function (el, i) {
      var n = i + 1, key = page + ':' + n, b = document.createElement('button'); b.type = 'button'; b.className = 'nbub'; b.textContent = n; b.setAttribute('aria-label', 'Note ' + n);
      var t = document.createElement('div'); t.className = 'ntip'; t.innerHTML = '<b>Note ' + n + '</b>'; t.appendChild(document.createTextNode(el.getAttribute('data-note')));
      b.addEventListener('click', function (e) { e.preventDefault(); e.stopPropagation(); var o = el.classList.contains('open'); items.forEach(function (x) { x.classList.remove('open'); }); if (!o) el.classList.add('open'); });
      el.appendChild(b); el.appendChild(t);
      var li = document.createElement('li'), cb = document.createElement('input'); cb.type = 'checkbox'; cb.id = 'nd' + n; cb.checked = !!done[key];
      var lab = document.createElement('label'); lab.htmlFor = 'nd' + n; lab.innerHTML = '<i>' + n + '</i>'; var sp = document.createElement('span'); sp.textContent = el.getAttribute('data-note'); if (cb.checked) sp.classList.add('done');
      cb.addEventListener('change', function () { done[key] = cb.checked; sp.classList.toggle('done', cb.checked); try { localStorage.setItem('notes-done', JSON.stringify(done)); } catch (e) {} });
      li.appendChild(cb); li.appendChild(lab); li.appendChild(sp); list.appendChild(li);
    });
    function set(on) { root.classList.toggle('notes', on); nbtn.setAttribute('aria-pressed', on); nbtn.querySelector('span').textContent = on ? nbtn.getAttribute('data-hide') : nbtn.getAttribute('data-show'); if (!on) items.forEach(function (x) { x.classList.remove('open'); }); }
    nbtn.addEventListener('click', function () { set(!root.classList.contains('notes')); });
    if (location.hash === '#notes') set(true);
  }
})();
