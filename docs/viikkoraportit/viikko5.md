# Viikko 5 

## Mitä tein tällä viikolla?

Viikko 5 oli projektin kannalta kriittinen vaihe, jossa siirryttiin kehityksestä testaus- ja viimeistelytyöhön. Painopiste oli kahdessa asiassa: tekoälyalgoritmin parantamisessa aiemman palautteen perusteella ja monipuolisen testausympäristön rakentamisessa. Nämä kaksi osa-aluetta kulkivat osittain käsi kädessä, sillä AI:n muutokset vaativat aina huolellista testausta ennen niiden lopullista käyttöönottoa.

Ensimmäinen suuri työ oli AI:n päätöksentekologiikan uudistaminen. Aiempi versio valitsi mallin yksinkertaisesti sen syvyyden perusteella, mikä ei aina johtanut parhaaseen lopputulokseen. Nyt toteutin ratkaisun, jossa tekoäly vertailee eri mallien voittoprosentteja ja valitsee niistä parhaiten menestyneen. Tätä varten kirjoitin uuden `select_best_model()`-funktion, joka käy läpi käytettävissä olevat mallit, tarkistaa niiden tilastot ja palauttaa parhaimman. Samalla otin käyttöön **5 kierroksen malli-persistenssin**: valittu malli pysyy käytössä viiden pelin ajan ennen mahdollista vaihtoa. Tämä vähentää mallin jatkuvaa vaihtelua ja antaa sille mahdollisuuden oppia vastustajan pelitavoista hieman pidemmällä aikavälillä. Lisäksi korjasin tilastojen päivityslogiikan niin, että tilastoja kerätään ainoastaan aktiivisesta mallista. Tämä tekee datasta johdonmukaisempaa ja helpommin analysoitavaa.

Toinen iso osa viikkoa kului testausympäristön kehittämiseen. Toteutin **integraatiotestit** (`test_integration.py`), jotka simuloivat kokonaisia pelisessioita ja testaavat eri moduulien välistä yhteistoimintaa, **suorituskykytestit** (`test_performance.py`), joilla mitataan pelin nopeutta, skaalautuvuutta ja muistinkäyttöä eri tilanteissa. 

Kaiken kaikkiaan viikon työ oli tasapaino teknisen kehityksen, käytettävyyden parantamisen ja laadunvarmistuksen välillä. Jokainen AI:lle tehty muutos käytiin läpi testauksen kautta, ja tuloksena järjestelmä on aiempaa vakaampi, johdonmukaisempi ja helpompi ylläpitää.

## Mitä opin?

Tällä viikolla opin, kuinka tärkeää on rakentaa monipuolinen testausstrategia, joka kattaa useita eri näkökulmia. Opin myös, että testien on hyvä toimia eri ympäristöissä ilman raskaita riippuvuuksia, sillä tämä tekee kehityksestä joustavampaa ja vähentää asennusongelmia.

Algoritmin kehityksen osalta ymmärsin, että paras ratkaisu ei aina ole teknisesti monimutkaisin tai “syvin” malli. Tilastollinen analyysi ja voittoprosenttien seuraaminen voivat antaa yksinkertaisemman mutta tehokkaamman lopputuloksen. Samalla opin tasapainoilemaan mallin vakauden ja sopeutumiskyvyn välillä: jos malli vaihtuu liian usein, se ei ehdi oppia vastustajaa, mutta jos se pysyy liian pitkään samana, se voi jäädä jumiin huonompaan strategiaan.

## Mikä oli vaikeaa?

Yksi suurimmista haasteista oli varmistaa, että testausympäristö toimii luotettavasti eri käyttöjärjestelmissä ja kehitysympäristöissä. Myös suorituskykytestien rajojen asettaminen ei ollut helppo, sillä piti päättää, mikä on “riittävän nopea” ja “riittävän kevyt” käytännön näkökulmasta.

## Mitä teen seuraavaksi?

Seuraavalla viikolla päivitän testausdokumentin kattamaan kaikki käytetyt testausstrategiat ja kirjoitan pelille selkeät käyttöohjeet.Mahdollisina jatkokehityskohteina harkitsen pelitilastojen tallentamista tiedostoon, graafisen käyttöliittymän prototyypin tekemistä ja uusien tekoälystrategioiden lisäämistä vertailuun.

## Käytetty aika

| Päivä | Käytetty aika |
|-------|---------------|
| 4.8.  | 5 h           |
| 5.8.  | 4 h           |
| 6.8.  | 6 h           |
| 7.8.  | 3 h           |
| 8.8.  | 2 h           |
| **Yhteensä** | **20 h** |
