# Käyttöohje - Oppiva Kivi-Sakset-Paperi Tekoäly

## Ohjelman suorittaminen

### Vaatimukset
- Python 3.8 tai uudempi
- Poetry riippuvuuksien hallintaan

### Asennus ja käynnistys

1. **Kloonaa repositorio:**
   ```bash
   git clone https://github.com/erarexhepi/Harjoitustyo.git
   cd Harjoitustyo
   ```

2. **Asenna riippuvuudet Poetry:llä (suositeltu):**

   ```bash
   pip install pytest
   ```

3. **Käynnistä peli:**
   ```bash
   python3 main.py
   ```

## Pelin käyttö

### Peruskomennot

Kun peli käynnistyy, voit käyttää seuraavia komentoja:

- **`kivi`** - Pelaa kivi
- **`paperi`** - Pelaa paperi
- **`sakset`** - Pelaa sakset
- **`help` tai `h`** - Näytä ohje
- **`stats` tai `s`** - Näytä yksityiskohtaiset tilastot
- **`quit` tai `q`** - Lopeta peli

### Syötteiden muoto

Peli hyväksyy seuraavat syötteet:

**Validi siirrot:**
- `kivi` (iso/pienkirjainväli ei väliä)
- `paperi` 
- `sakset`

**Komennot:**
- `help`, `h`
- `stats`, `s` 
- `quit`, `q`

Peli ohittaa tyhjät syötteet ja välilyönnit automaattisesti.

### Pelin kulku

1. **Kierroksen aloitus:** Peli näyttää kierrosnumeron ja pyytää sinua tekemään siirron
2. **Siirtojen näyttö:** Molempien siirrot näytetään emoji-symboleilla
3. **Tuloksen ilmoitus:** Peli kertoo kuka voitti ja miksi
4. **Tilastojen päivitys:** Nykyiset voittotilastot näytetään kierroksen lopussa
5. **AI:n tila:** Näytetään mikä malli AI:lla on käytössä

### Tilastot ja seuranta

**Perustilastot (näytetään jokaisen kierroksen jälkeen):**
- Voittotilanne (Sinä vs AI)
- Voittoprosenttisi
- AI:n nykyinen malli ja kierrosten määrä

**Yksityiskohtaiset tilastot (`stats`-komento):**
- Kaikkien pelattujen kierrosten määrä
- Voitot, häviöt ja tasapelit prosentteina
- AI:n oppimistilastot eri malleille
- Viimeisimmät 5 peliä
- AI:n nykyinen aktiivinen malli

### AI:n toiminta

**Oppiminen:**
- AI seuraa siirtoja ja tallentaa historiaa
- Se yrittää löytää kuvioita 1-5 siirron pituisista sekvensseistä
- AI valitsee parhaiten menestyneen mallin 5 kierroksen jaksoissa

**Mallit:**
- **Aste 1:** Ennustaa seuraavan siirron edellisen perusteella
- **Aste 2:** Käyttää kahta edellistä siirtoa
- **Aste 3-5:** Käyttää pidempää historiaa tarkempiin ennusteisiin

## Testien suorittaminen

```bash
python3 test_markov.py

python3 test_integration.py

python3 test_performance.py
```

### Testikattavuus
```bash
 python3 -m pytest --cov=src --cov-report=html --cov-report=term test_*.py
```

## Lisätiedot

Lisätietoja algoritmin toiminnasta ja teknisistä yksityiskohdista löydät:
- `docs/toteutusraportti.md` 
- `docs/testausraporti.md`
- `docs/maarittelydokumentti.md`