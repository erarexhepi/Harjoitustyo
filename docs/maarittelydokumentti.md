# Määrittelydokumentti

## Projektin nimi
Oppiva tekoäly: Kivi-sakset-paperi

## Opinto-ohjelma
Tietojenkäsittelytieteen kandidaatti (TKT)

## Dokumentaation kieli
Suomi


## Käytettävä ohjelmointikieli
Python

## Muut hallitsemani kielet
Java, JavaScript, TypeScript

Voin tarvittaessa vertaisarvioida näillä kielillä toteutettuja projekteja.


## Kuvaus ongelmasta
Toteutetaan Kivi-sakset-paperi -peli, jossa käyttäjä pelaa tietokonetta vastaan. Tietokoneen pelaamaa siirtoa ohjaa oppiva tekoäly, joka analysoi käyttäjän aiempia valintoja ja pyrkii ennustamaan, mitä käyttäjä pelaa seuraavaksi. Tekoälyn ennustus perustuu Markovin ketjuihin.


## Algoritmit ja tietorakenteet

- **Markovin ketjut (1. ja 2. asteen)**: Pelaajan aiemmista siirroista lasketaan todennäköisyyksiä seuraavalle siirrolle.
- **Sanakirjat / hash mapit (Python `dict`)**: Siirtymätaulujen toteutus ja todennäköisyyksien tallennus.


## Syötteet

- Pelaajan tekemät siirrot (`kivi`, `sakset`, `paperi`)
- Aiemmat siirrot tallennetaan tekoälyn mallin päivittämiseksi

## Ohjelman toiminta

1. Käyttäjä tekee valinnan (kivi, sakset tai paperi)
2. Tekoäly analysoi käyttäjän edellisiä siirtoja
3. Tekoäly valitsee todennäköisyyksien perusteella siirron, joka voittaa todennäköisimmän käyttäjän siirron
4. Tulostetaan molempien siirrot ja päivitetään oppimismalli


## Aika- ja tilavaativuudet

- Markovin ketjun päivitys: O(1) (sanakirjan päivitys)
- Seuraavan siirron ennustaminen: O(1) (haetaan siirtymät nykytilasta)
- Muistin käyttö: O(n), missä n on eri siirtymätilojen määrä 


## Harjoitustyön ydin

Projektin ydin on toteuttaa oppiva tekoäly Kivi-sakset-paperi -peliin hyödyntämällä Markovin ketjuja. Tekoälyn tulee sopeutua käyttäjän pelityyliin ja ennustaa tämän seuraavaa siirtoa tehokkaasti. Työn tärkein osa on siirtymätaulujen rakentaminen ja niiden käyttö siirtojen ennustamiseen.


## Lähteet

- Wikipedia: [Markov chain](https://en.wikipedia.org/wiki/Markov_chain)
- GeeksForGeeks: [Markov Chains and Transition Probability](https://www.geeksforgeeks.org/machine-learning/markov-chain/)
- Kurssimateriaali
