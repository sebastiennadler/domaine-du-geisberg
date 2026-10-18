#!/bin/bash
# Télécharge les images et les pages de l'ancien site dans ce dossier.
cd "$(dirname "$0")"
mkdir -p images pages
while read -r u; do [ -n "$u" ] && curl -sL --retry 2 -o "images/$(basename "$u")" "$u" && echo "ok  $(basename "$u")"; done < images.txt
for p in "" le-domaine gites-ruraux-moselle tourisme-et-loisirs-moselle reservation-gite-moselle visite-virtuelle mentions-legales en en/domain en/cottage en/tourism-and-leisure en/reservation de de/tourismus-und-freizeit de/reservierung es es/turismo-y-ocio es/reserva; do
  n="${p:-index}"; n="${n//\//_}"; curl -sL -o "pages/$n.html" "http://www.domainedugeisberg.fr/$p/" && echo "ok  page $n"
done
echo "Terminé : $(ls images | wc -l) images, $(ls pages | wc -l) pages."
