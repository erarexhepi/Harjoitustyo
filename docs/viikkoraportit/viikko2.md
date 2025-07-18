# Viikko 2 - Harjoitustyön raportti

## Mitä tein tällä viikolla?

Tällä viikolla rakensin simppelin version kivi-sakset-paperi -pelistä, jossa tekoäly (AI) oppii pelaajan siirroista Markovin ketjujen avulla. Toteutin kolme pääosaa:

- **`markov.py`**: AI:n ydinlogiikka. Se tallentaa pelaajan siirtohistorian ja yrittää ennustaa seuraavan siirron perustuen edellisiin siirtymiin.
- **`game.py`**: Pääohjelma, joka lukee pelaajan syötteen, kysyy AI:lta vastauksen ja kertoo, kumpi voitti.
- **`test_markov.py`**: Yksikkötestit, joilla varmistan AI:n logiikan oikeellisuuden (historian tallennus, ennustus ja vastasiirron logiikka).

## Mitä opin?

- Miten Markovin ketjuja voi käyttää yksinkertaisen pelaajamallin rakentamiseen.
- Miten `pytest` toimii ja miten voin lisätä testikattavuutta.
- Miten siirrot voidaan mallintaa niin, että AI parantaa suoritustaan ajan myötä.

## Mikä oli vaikeaa?

- Aluksi minulla oli hankaluuksia pytestin kanssa
- Yksi haaste oli AI:n logiikan testaaminen siten, että tulokset olisivat toistettavia. Koska ennustaminen perustuu satunnaisuuteen silloin kun historiadataa ei ole, testien tekeminen vaati erityistä huomiota tilanteisiin, joissa AI:n pitää tehdä valinta arpomalla. Tämä edellytti, että ennustuksen ja vastasiirron logiikka eriytettiin selkeästi, jotta satunnaisuus ei sotkisi testien tuloksia.

## Mitä teen seuraavaksi?

- Teen pelistä visuaalisesti hienomman
- Lisään pelin pääsilmukan, jotta peliä voi pelata useamman kierroksen ajan.
- Kirjaan pelitilastot: voitot, tappiot ja tasapelit.
- Mahdollisesti teen yksinkertaisen käyttöliittymän.
- Parannan testikattavuutta kattamaan lisää erikoistapauksia.

## Käytetty aika
| Päivä | Käytetty aika |
|-------|---|
| 16.7. | 4 |
| 18.7. | 3 |
| 19.7.| 1 |
| **Yhteensä** | **8 h** |

