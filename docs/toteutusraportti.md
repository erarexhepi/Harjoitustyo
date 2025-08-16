# Toteutusdokumentti

## Ohjelman yleisrakenne

### Moduulirakenne

Projekti on jaettu selkeisiin osiin, joilla jokaisella on oma vastuunsa:

- **markov.py** – sisältää tekoälyn logiikan ja Markov-mallien toteutuksen  
- **game.py** – vastaa käyttöliittymästä, peliloopista ja tilastojen hallinnasta  
- **main.py** – ohjelman käynnistyspiste, joka kokoaa kaiken yhteen  

Testipuolella on omat tiedostonsa yksikkötesteille, integraatiotesteille ja suorituskykytesteille, jotta ohjelman toiminta voidaan varmistaa eri näkökulmista.


- **MarkovAI-luokka (`markov.py`)**  
  Tämä luokka toteuttaa varsinaisen tekoälyalgoritmin. Se hallitsee siirtymätauluja, kerää oppimiseen tarvittavat tilastot ja pystyy tekemään ennusteita pelaajan seuraavista siirroista.

- **VisualGame-luokka (`game.py`)**  
  Vastaa pelin käyttöliittymästä ja ohjaa pelin kulkua. Se toimii linkkinä tekoälyn ja pelaajan välillä, huolehtii kierroksista sekä tulosten näyttämisestä.

- **GameStats-luokka (`game.py`)**  
  Pitää kirjaa pelin tilastoista, kuten voittoprosenteista ja pelihistoriasta. Näiden avulla voidaan myöhemmin analysoida tekoälyn ja pelaajan suorituksia.

---

## Algoritmien toteutus ja analyysi

### Hierarkkinen Markov-malli

Perinteinen Markov-ketju ottaa huomioon vain yhden edellisen siirron. Tässä projektissa tekoälylle annettiin enemmän ”muistia”: se seuraa samanaikaisesti useita eri syvyyksiä (1–5 edellistä siirtoa). Tämä tekee mallista huomattavasti tarkemman, koska se pystyy havaitsemaan monimutkaisempia toistuvia kuvioita pelaajan toiminnassa.  

Käytännössä jokaiselle syvyydelle tallennetaan, mitä siirtoa seuraavaksi on todennäköisimmin seurannut. Kun pelaaja tekee uuden siirron, tekoäly päivittää taulunsa ja hyödyntää niitä ennustaessaan tulevaa.

**Ennustusprosessi** etenee syvimmästä mahdollisesta tasosta yksinkertaisimpaan. Jos esimerkiksi viiden siirron kuvio löytyy historiasta, sitä käytetään. Jos ei, tekoäly tarkistaa neljän, kolmen jne. tasot, kunnes löytyy sopiva kuvio.

### Aikavaativuus

Algoritmi on suunniteltu tehokkaaksi. Jokainen päivitys ja ennustus tapahtuu käytännössä vakioajassa, koska sanakirjahaut ja pienten taulukoiden käsittely on nopeaa. Yhden kierroksen suoritus kestää vain millisekunteja, mikä tekee pelaamisesta sujuvaa.

### Tilavaativuus

Koska mahdollisia siirtymiä on rajallisesti, tallennettavia yhdistelmiä kertyy lopulta varsin vähän. Teoreettisesti enimmäismäärä on hieman yli tuhat siirtymää, mikä on nykyaikaiselle tietokoneelle mitätön määrä. Käytännössä tilankäyttö kasvaa lineaarisesti pelattujen kierrosten määrän mukana.

---

## Mallivalinta

Koska tekoäly seuraa useita malleja yhtä aikaa, sen on päätettävä, minkä ennusteen varaan se kulloinkin pelaa. Tätä varten se seuraa eri syvyyksien voittoprosentteja. Jos jokin malli on jatkuvasti onnistunut hyvin, sitä suositaan.  

Lisäksi valinta pysyy voimassa viiden kierroksen ajan, jotta tekoäly ei vaihda mallia liian usein. Tämä tuo peliin tasapainoa ja tekee tekoälyn käyttäytymisestä luonnollisempaa.

---

## Suorituskyky ja vertailu

Toteutettua hierarkkista mallia voidaan verrata kolmeen vaihtoehtoon:

1. **Yksinkertainen Markov-ketju (1 aste)**  
   – Hyvin nopea, mutta ei osaa tunnistaa pidempiä kuvioita.  

2. **Hierarkkinen Markov (1–5 astetta, nykyinen ratkaisu)**  
   – Löytää monimutkaisia kuvioita ja toimii silti tehokkaasti.  


Vertailun perusteella valittu ratkaisu tarjoaa parhaan kompromissin: se on riittävän tarkka mutta säilyttää suorituskyvyn kevyenä.

---

## Työn rajoitukset ja parannusehdotukset

Nykyinen toteutus toimii hyvin, mutta siinä voisi olla muutamia muutamia kehityskohteita:

- **Muistinhallinta**: Historia kasvaa rajatta. Tämä voidaan rajoittaa esimerkiksi tuhat kierroksen liukuvaan ikkunaan.  
- **Mallin arviointi**: Nyt käytössä on yksinkertainen voittoprosentti. Tilastollisesti hienostuneemmat menetelmät, kuten luottamusvälit, voisivat tehdä arvioinnista tarkemman.  

---

## Jatkokehitysmahdollisuuksia

- **Mukautuva syvyys**: Tekoäly voisi säätää maksimisyvyyttään sen mukaan, kuinka monimutkaisia kuvioita pelaajalla on tapana käyttää.  
- **Aikapainotus**: Uudemmat siirrot voitaisiin painottaa enemmän kuin vanhat, jolloin tekoäly reagoisi herkemmin muutoksiin pelaajan strategiassa.  

---

## LLM:n käyttö

Käytin apuna ChatGPT:tä dokumentaation laatimisessa. Sen avulla sain karsittua kirjoitusvirheitä ja muokattua jo valmista teksitäni selkeämmiksi.

---


## Lähteet

1. **Markov, A. A.** (1913). *An Example of Statistical Investigation of the Text Eugene Onegin Concerning the Connection of Samples in Chains*. Classical foundation for Markov chain theory.

2. **Feller, W.** (1968). *An Introduction to Probability Theory and Its Applications, Volume 1*, 3rd edition. Comprehensive mathematical background for transition probability calculations.

3. **Russell, S., Norvig, P.** (2020). *Artificial Intelligence: A Modern Approach*, 4th edition. Chapter 15: Probabilistic reasoning over time. Theoretical foundation for temporal pattern recognition.

4. **Wikipedia**: [Markov chain](https://en.wikipedia.org/wiki/Markov_chain) - Mathematical definitions and properties used in algorithm design.


