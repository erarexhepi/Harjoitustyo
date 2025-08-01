# Viikko 4 - Harjoitustyön raportti

## Mitä tein tällä viikolla?

Viikko 4 oli projektin intensiivisin vaihe, jossa toteutin viikon 3 suunnitelman hierarkkisesta Markov-mallista. Aloitin uudelleenkirjoittamalla markov.py tiedoston kokonaan siten, että AI seuraa nyt samanaikaisesti 1-5 siirron pituisia historiasekvenssejä. 

Käyttökokemuksen parantamiseen keskityin tekemällä pelistä visuaalisesti kiinnostavan. Lisäsin emojeita, värejä ja selkeän pelin kulun.


## Mitä opin?

Ymmärsin miten eri syvyystasot voivat antaa eri tarkkuudella ennusteita ja miten näitä tulisi priorisoida. Aste 1 (edellinen siirto) antaa ennusteita usein mutta matalalla tarkkuudella, kun taas aste 3-5 antavat harvemmin mutta tarkempia ennusteita. Mallin pitää osata käyttää aina parasta käytettävissä olevaa tietoa.

Teknisesti opin paljon Python-modulaarisen arkkitehtuurin hallinnasta Poetry-ympäristössä. Import-polkujen hallinta ja modulaarisuus olivat aluksi haasteellisia, mutta lopputulos on selkeä kolmetiedostoinen rakenne joka on helppo ylläpitää.

## Mikä oli vaikeaa?
Hierarkkisen mallin logiikka oli odotettua monimutkaisempi. Erityisesti voittotilastojen päivityslogiikka aiheutti päänvaivaa.

Päädyin ratkaisuun jossa tilastoja päivitetään vain kun ennuste oli mahdollinen, mutta tämä vaati huolellista testausta.

## Mitä teen seuraavaksi?

Dokumentaation kirjoittaminen on seuraava prioriteetti. Projekti tarvitsee selkeän dokumentaation, joka selittää mallin toimintaperiaatteen ja käyttöohjeet. Lisäksi harkitsen pelitilastojen tallentamista tiedostoon, jotta pelaajan kehitystä voisi seurata pidemmällä aikavälillä.

## Käytetty aika

Hierarkkisen mallin suunnittelu ja toteutus veivät suurimman osan ajasta, kun taas käyttöliittymän parannus ja testien kirjoittaminen veivät loput.

| Päivä | Käytetty aika |
|-------|---|
| 28.7 | 4 |
| 30.7 | 3 |
| 31.7 | 5 |
| 1.8  | 2 |
| **Yhteensä** | **14 h** |