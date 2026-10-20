/* Domaine du Geisberg — appliqué avant le premier affichage : classe js + thème clair/sombre mémorisé (évite un flash). */
(function () {
  var d = document.documentElement;
  d.className = d.className.replace('no-js', 'js');
  try {
    var t = localStorage.getItem('geisberg-theme');
    if (t === 'dark' || t === 'light') d.setAttribute('data-theme', t);
  } catch (e) {}
})();
