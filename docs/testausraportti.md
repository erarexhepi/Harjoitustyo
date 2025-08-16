# Testausdokumentti

## Yleiskuvaus

Projektin testausstrategia koostuu kolmesta testauksesta: yksikkötesteistä, integraatiotesteistä ja suorituskykytesteistä. 

## Testikattavuusraportti

### Yksikkötestien kattavuus

**Tiedosto: `test_markov.py` → `src/markov.py`**
- **Rivikattavuus**: 100% (81/81 riviä)
- **Funktioiden kattavuus**: 100% 

**Tiedosto: `src/game.py`**
- **Rivikattavuus**: 46% (74/160 riviä)
- **Syy matalalle**: Käyttöliittymäkoodi, print-lauseet, input-käsittely

**Rivikattavuusraportti:**
**Testatut komponentit:**
- `MarkovAI`-luokan kaikki julkiset metodit
- Siirtymätaulujen päivityslogiikka
- Ennustusalgoritmit eri syvyystasoilla
- Voittotilastojen laskenta
- Mallin valintalogiikka

**Rivikattavuusraportti (`pytest --cov=src`):**
```
Name              Stmts   Miss  Cover
-------------------------------------
src/__init__.py       0      0   100%
src/game.py         160     86    46%
src/markov.py        81      0   100%
-------------------------------------
TOTAL               241     86    64%


```

## Yksikkötestaus

### Testatut funktionaliteetit

**1. Perusominaisuudet (`test_basic_initialization`)**
- Testattu että `MarkovAI` alustuu oikein syvyydellä 1-5
- Varmistettu että historia on tyhjä alussa
- Tarkistettu että kaikki siirtymätaulut luodaan

**2. Historian päivitys (`test_history_updates`)**
- Testattu yksittäisen siirron lisääminen
- Varmistettu siirtymätaulujen oikea päivitys
- Tarkistettu eri syvyystasojen toiminta

**3. Ennustusalgoritmit (`test_prediction_logic`)**
- Testattu ennusteiden generointi eri syvyyksillä
- Varmistettu että ennusteet ovat valideja siirtoja
- Tarkistettu hierarkkinen prioriteetti (syvempi ensin)

**4. Vastaliikkeen validius (`test_counter_move_validity`)**
- Testattu 100 satunnaista vastaliikettä
- Varmistettu että kaikki palautetut siirrot ovat valideja
- Tarkistettu toiminta tyhjällä ja täytetyllä historialla

**5. Voittolaskenta (`test_win_calculation`)**
- Testattu kaikki 9 siirtokombinaatiota systematically:
  - AI voittaa: kivi→paperi, paperi→sakset, sakset→kivi
  - Pelaaja voittaa: kivi→sakset, paperi→kivi, sakset→paperi  
  - Tasapelit: kivi→kivi, paperi→paperi, sakset→sakset

### Testisyötteet

**Deterministiset syötteet:**
```python
# Yksinkertainen kuvio
["kivi", "paperi", "sakset", "kivi"]

# Toistuva kuvio
["kivi", "paperi", "sakset"] * 20

# Samat siirrot
["kivi"] * 50
```

**Satunnaiset syötteet:**
- 1000 kierroksen satunnaiset pelit eri strategioita vastaan

## Integraatiotestit

### Testattu vuorovaikutus (`test_integration.py`)

**1. GameStats-integraatio**
- Testattu tilastojen tallentaminen ja hakeminen
- Varmistettu voittoprosenttien oikea laskenta
- Tarkistettu pelimäärän ja -historian päivitys

**2. VisualGame-integraatio**
- Testattu pelin alustaminen
- Varmistettu voittajan määritys kaikilla siirtokombinaatioilla
- Simuloitu kokonaisia pelisessioita

**3. AI-Game vuorovaikutus**
- Testattu AI:n oppiminen 10-kierroksen peleissä
- Varmistettu mallien vaihtuminen 5-kierroksen jaksoissa
- Tarkistettu tilastojen johdonmukaisuus

### Pitkän pelin simulaatio

**Testattu strategiat:**
1. **Satunnainen**: `random.choice(["kivi", "paperi", "sakset"])`
2. **Kuvio**: `["kivi", "paperi", "sakset"][round % 3]`
3. **Kivenvastustaja**: Aina `"paperi"`
4. **Mukautuva**: Vaihtaa strategiaa 500 kierroksen jälkeen


## Suorituskykytestit

### Aikavaativuusmittaukset (`test_performance.py`)


Testien tulokset vahvistivat että:
- Historian päivitys: O(1)
- Ennustuksen generointi: O(1) 
- Pelin nopeus: Alle 5ms per kierros

Yksityiskohtaiset mittaustulokset saatavissa ajamalla:
`python3 test_performance.py`

**2. Ennustuksen nopeus:**

-
**3. Kokonaisen pelin suorituskyky:**

### Skaalautuvuustestit

**Eri syvyystasojen vertailu:**
-

**Muistinkäyttö:**

-
## Erityistestaus

### Tarkkuustestit


 **Satunnaisen vastustajan käsittely:**
 -


### Rasitustestit

**1. Muistivuotojen havaitseminen:**
- 10,000 kierroksen testi
- Ei havaittuja muistivuotoja




### Ihmispelaajien kanssa

-

### Graafinen analyysi

-

## Testien toistaminen

### Automaattiset testit
```bash

# Yksikkötestit
python test_markov.py

# Integraatiotestit
python test_integration.py

# Suorituskykytestit  
python test_performance.py

# Kattavuusraportti
pytest --cov=src --cov-report=html
```

### Manuaalinen testaus
```bash
# Interaktiivinen peli
python main.py

# Tilastojen seuranta
# Pelaa 20+ kierrosta ja tarkkaile AI:n oppimista
```

## Rajoitukset ja tunnetut ongelmat

### Nykyiset rajoitukset

1. **Maksimi historianpituus**: Ei rajaa, voi kasvaa suureksi pitkissä peleissä
2. **Kylmäkäynnistys**: AI tarvitsee 5-10 kierrosta oppimiseen
3. **Yksinkertainen vastustajamalli**: Ei huomioi pelaajan psykologiaa

### Parannusehdotukset testauksen perusteella

1. **Histarian optimointi**: Rajoita muistin käyttöä vanhempien siirtymien poistamisella
2. **Nopean oppimisen**: Käytä Bayesian-päivitystä alkuvaiheessa
3. **Monimutkaisten kuvioiden tunnistus**: Lisää temporaalista analyysiä

## Yhteenveto
-
