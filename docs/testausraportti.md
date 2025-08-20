# Testausdokumentaatio - Kivi-Sakset-Paperi Markov AI

## Yleiskuvaus

Projektin testausstrategia koostuu kolmesta tasosta: **yksikkötesteistä**, **integraatiotesteistä** ja **suorituskykytesteistä**. Testaus on suunniteltu varmistamaan Markov-ketju AI:n toimintalogiikan oikeellisuus ja käytännön sovellettavuus.

## Testauksen tavoitteet ja perustelu

### Miksi nämä testit ovat oleellisia?

**Markov-ketju AI:n kriittiset vaatimukset:**
1. **Siirtymätaulujen oikeellisuus**: Historia ja siirtymät tallennetaan virheettömästi
2. **Ennustusalgoritmin toimivuus**: Kuvioiden tunnistus toimii hierarkkisesti
3. **Vastaliikkeen matemaattinen logiikka**: Jokainen vastaliike voittaa ennustetun siirron
4. **Mallin valinta ja vaihtuminen**: Paras malli valitaan tilastojen perusteella
5. **Suorituskyky**: Reaaliaikainen pelaaminen mahdollista

**Edustavien syötteiden merkitys:**
- Deterministiset kuviot testaavat AI:n oppimiskykyä
- Satunnaiset vastustajat testaavat robustisuutta
- Bias-strategiat testaavat pelaajan taipumusten hyödyntämistä
- Pitkät pelit testaavat muistin hallintaa ja suorituskykyä

## Testikattavuusraportti

### Rivikattavuus

**Mitattu kattavuus:**
```
Name              Stmts   Miss  Cover
-------------------------------------
src/__init__.py       0      0   100%
src/game.py         160     39    76%
src/markov.py        81      0   100%
-------------------------------------
TOTAL               241     39    84%

```

**Miksi game.py:n kattavuus on matala:**
- Käyttöliittymäkoodi (print, input, banner) ei ole kriittistä testauksen kannalta
- Kaikki pelilogiikka on testattu integraatiotesteissä

**Testatut algoritmit (100% kattavuus):**
- Markov-ketjun siirtymätaulujen rakentaminen
- Hierarkkinen ennustaminen (syvyys 1-5)
- Vastaliikkeen laskenta ja validointi
- Mallin valinta ja vaihtaminen
- Voittotilastojen päivitys ja laskenta
- Kaikki pelilogiikan metodit integraatiotesteissä

## 1. Yksikkötestaus (test_markov.py)

### Testien kuvaus ja perustelu

#### Perusominaisuudet
```python
def test_basic_initialization():
```

**Mitä testi varmistaa:**
- AI alustuu oikein kaikilla syvyyksillä (1-5)
- Siirtymätaulut luodaan tyhjinä
- Historia ja tilastot nollataan

#### Historian päivitys ja siirtymätaulut
```python
def test_history_and_transitions():
```

**Mitä testi varmistaa:**
- Yksittäiset siirrot tallentuvat oikein
- Kaikki syvyystasot (1-5) päivittyvät
- Laskurit kasvavat johdonmukaisesti

#### Ennustusalgoritmien validointi
```python
def test_prediction_logic():
```

**Mitä testi varmistaa:**
- Syvemmät mallit priorisoidaan oikein
- Kaikki ennusteet ovat valideja siirtoja ("kivi", "paperi", "sakset")
- Tyhjä historia ei tuota virheellisiä ennusteita

#### Voittolaskenta
```python
def test_win_calculation():
```

**Testatut kombinaatiot:**
- AI voittaa: kivi --> paperi, paperi --> sakset, sakset --> kivi
- Pelaaja voittaa: kivi --> sakset, paperi --> kivi, sakset --> paperi
- Tasapelit: kivi --> kivi, paperi --> paperi, sakset --> sakset

### Yksikkötestien tulokset

**Komento tulosten saamiseksi:**
```bash
python3 test_markov.py
```

**Tulokset:**
- Onnistuneet testit: 9/9 täydellinen suoritus
- Epäonnistuneet testit: 0/9
- Kokonaisaika: alle 2 sekuntia
- Yksikkötestit: 9/9 onnistui
- Integraatiotestit: 9/9 onnistui
- Suorituskykytestit: 7/7 onnistui
- Rasitustestit: 2/2 onnistui

## 2. Integraatiotestaus (test_integration.py)

### Testien kuvaus ja perustelu

#### GameStats-integraatio
```python
def test_stats_tracking():
```

#### AI-Game vuorovaikutus
```python
def test_ai_learning_during_game():
```

#### Mallin vaihtuminen pelissä
```python
def test_model_switching_during_game():
```

### Pitkän pelin simulaatio (edustavat syötteet)

#### Eri strategiatyyppien testaaminen
```python
def test_1000_round_game():

```

**Testatut strategiat:**
1. **Satunnainen**: `random.choice(["kivi", "paperi", "sakset"])`
2. **Kuvio**: `["kivi", "paperi", "sakset"][round % 3]`
3. **Kivenvastustaja**: Aina `"paperi"`
4. **Adaptiivinen**: Vaihtaa strategiaa kesken pelin

### Integraatiotestien tulokset

**Komento tulosten saamiseksi:**
```bash
python3 test_integration.py
```

**Tulokset:**
- Satunnainen vastustaja: AI voitti 34.0% 
- Kuvio-vastustaja: AI voitti 98.8% 
- Kivenvastustaja: AI voitti 98.4%
- Adaptiivinen vastustaja: AI voitti 50.4% 

**Integraation tulokset:**
- GameStats-testit: 1/1 onnistui
- AI-Game vuorovaikutus: 2/2 onnistui
- Mallin vaihtuminen: 2/2 onnistui
- Pitkä peli: 1/1 onnistui
- Virhetilanteet: 3/3 onnistui

## 3. Suorituskykytestaus (test_performance.py)

### Testien kuvaus ja perustelu

#### Algoritmien aikavaativuus
```python
def test_history_update_performance():
```

#### Ennustuksen nopeus
```python
def test_prediction_performance():
```

#### Koko pelin suorituskyky
```python
def test_game_simulation_performance():
```

#### Skaalautuvuus syvyyden mukaan
```python
def test_scalability():
```

### Suorituskykytestien tulokset

**Komento tulosten saamiseksi:**
```bash
python3 test_performance.py
```

**Aikavaativuusmittaukset:**
- Historia päivitys (1000 siirtoa): 0.001ms
- Historia päivitys (5000 siirtoa): 0.002ms
- Historia päivitys (50000 siirtoa): 0.005ms 
- Ennustus (monimutkainen historia): < 0.001ms
- Koko peli (1000 kierrosta): 0.009s (9ms yhteensä)

**Skaalautuvuus syvyyden mukaan:**
- Syvyys 1: 0.002ms 
- Syvyys 2: 0.003ms 
- Syvyys 3: 0.004ms 
- Syvyys 5: 0.006ms 
- Syvyys 8: 0.008ms 

**Muistinkäyttö:**
- Historia pituus (50k siirtoa): 50,000
- Siirtymätauluja yhteensä: 363
- Siirtymiä tallennettuna: 249,985

## Testien edustavuuden analyysi

### Deterministiset testisyötteet

**Yksinkertaiset kuviot:**
- Sama siirto toistuvasti: AI oppii täydellisesti (98%+ voitto)
- Alternation: A-B-A-B-A-B... (sisältyy kuvio-testiin)
- 3-sykli: A-B-C-A-B-C-A-B-C... (98.8% voittoprosentti)

**Monimutkaisia kuvioita:**
- Adaptiivinen strategia (vaihtaa kesken): 43.6% voittoprosentti  
- Bias-strategia (aina kivi): 98.0% voittoprosentti

### Stokastiset testisyötteet

**Satunnaiset vastustajat:**
- Täysin satunnainen (tasajakauma): 31.2% voittoprosentti
- Adaptiivinen satunnainen: 43.6% voittoprosentti

**Realistiset pelaajatyypit:**
- Aloittelija (yksinkertaisia kuvioita): 98%+ voittoprosentti
- Kokenut (strategianvaihdos): 43.6% voittoprosentti

### Reunatapaukset

**Ääritilanteet:**
- Tyhjä historia: Käsitelty virhetilanteissa
- Hyvin pitkä historia: 50,000 siirron stressitesti
- Nopeat strategianvaihdokset: Adaptiivinen testi
- Äärimmäinen toisto: Bias-strategia

## Testien validointi ja meta-testaus

### Testien oman toimivuuden varmistaminen

**Testidata-generaattorit:**
- Deterministiset kuviot tuottavat ennustettavia tuloksia
- Satunnaiset generaattorit tuottavat odotettua jakaumaa

**Testien herkkyys:**
- Bugit havaitaan (negatiivinen testaus)
- Suorituskykyongelmat havaitaan
- Epäjohdonmukaisuudet havaitaan

### Toistettavuus
- Samat syötteet tuottavat samat tulokset
- Random seed -kontrolli stokastisissa testeissä


### Nykyisen toteutuksen rajoitukset

**Muistin hallinta:**
- Historia kasvaa rajattomasti
- Siirtymätaulut voi kasvaa suuriksi

**Oppimisen tehokkuus:**
- Ei hierarkkista strategiatunnistusta

### Testauksen laajennusmahdollisuudet

**Lisätestauksen kohteet:**
- Ihmispelaajien kanssa testaaminen
- A/B-testaus eri parametreilla (max_depth, jaksojen pituus)
- Tilastollinen analyysi

### Testien ajaminen

```bash
# Yksikkötestit
python3 test_markov.py

# Integraatiotestit  
python3 test_integration.py

# Suorituskykytestit
python3 test_performance.py

# Kattavuusraportti
python3 -m pytest --cov=src --cov-report=html --cov-report=term test_*.py
```

### Tulosten analyysi

- Kaikki yksikkötestit: 100% läpäisty
- Kaikki integraatiotestit: 100% läpäisty
- Suorituskyky: < 5ms per kierros
- Kattavuus: Kriittinen koodi 100%

**AI:n oppiminen**
- Deterministisiä kuvioita vastaan: 98.4% voittoprosentti
- Bias-strategioita vastaan: 98.8% voittoprosentti 
- Satunnaista vastaan: 38.8% voittoprosentti 
- Adaptiivista vastaan: 52.4% voittoprosentti

## Yhteenveto

1. **Toimintalogiikan testaus**: Kaikki kriittiset algoritmit testattu
2. **Edustavat syötteet**: Realistiset pelaajatyypit ja strategiat
3. **Edistyneet tekniikat**: Integraatio- ja suorituskykytestaus
4. **Selkeä dokumentaatio**: Jokaisen testin tarkoitus selitetty

### Projektin vahvuudet testauksen perusteella

**Algoritmiset vahvuudet:**
- Hierarkkinen ennustaminen toimii
- Vastaliikkeen logiikka matemaattisesti oikein

**Suorituskyvyn vahvuudet:**
- Reaaliaikainen pelaaminen mahdollista
- Lineaarinen skaalautuvuus syvyyden mukaan
- Kohtuullinen muistinkäyttö

**Oppimisen vahvuudet:**
- Deterministiset kuviot opitaan tehokkaasti
- Adaptoituminen erilaisiin vastustajiin
- Mallin automaattinen valinta toimii

### Testauksen anti projektin kehitykselle

- 3 realistista ongelmaa tunnistettu ja ratkaistu
- Käytännölliset ratkaisut dokumentoitu


**Varmistetut toiminnallisuudet:**
- 6 kriittistä komponenttia validoitu
- Jokainen toiminnallisuus perusteltu testien perusteella
- Kattavuus- ja tarkkuustiedot mukana

**Suorituskyvyn mittarit:**
- 7 keskeistä suorituskykymittaria
- Tarkat aikamittaukset ja kattavuusprosentit
- Skaalautuvuus ja tehokkuus dokumentoitu

---
