Title: Šestý sraz - Travis CI
Date: 2018-11-06 21:17:00
Modified: 2018-11-16 21:17:00
Author: Zuzana Kletzanderová

V úvodu našeho dalšího srazu jsme si ujasnily komunikaci týmu kolem celého projektu. Hlavní bod diskuze - neurážej se kvůli opravě tvého kódu! :) Dále aby byl lepší přehled o tom kdo na čem pracuje, v jakém je to stavu a aby byl *celkově* lepší přehled co se v projektu děje, jsme se domluvily, že budeme vše řešit především na Slacku.

Hlavním bodem našeho setkání bylo, pod vedením Jirky, jak funguje integrace GitHub-u a jak nám pomůže v testování **Travis CI**.

Ze začátečnického kurzu už víme, jak může vypadat test na kód, který napíšeme. Například pomocí příkazu 'assert'. Testy rozdělujeme na manuální a automatické (pytest). Hlavní je to, že testy umožňují říct, zda je kód v pořádku, nebo jestli s ním musíme dále něco dělat. S testy nečekáme až bude finální verze, ale testujeme už jednotlivé změny, které děláme.

A teď něco k **Travis CI** (Continuous Integration):

- je to služba, která spouští automatizované testy na GitHubu, které běží kontinuálně s tím co jsme na GitHub-u přidaly 
- [travis-ci.org](https://travis-ci.org) má službu poskytovanou zdarma pro veřejné repozitáře, [travis-ci.com](https://travis-ci.com) je placená verze pro privátní účely
-  a co Travis dělá? Travis si na testování vytvoří virtuální počítač, stáhne si zdrojový kód a v rámci zdrojového kódu provede příkazy, které chceme
- Travis se konfiguruje pomocí souboru `.travis.yml` umístěným v kořenovém adresáři projektu. V souboru je uvedeno vše potřebné pro správné spuštění testů, včetně instalace závislostí atd. Mimo jiné se jedná o jazyk pro jaký se má nastavit prostředí, v jaké verzi (těch může být kolik potřebujeme), instalace závislostí (v našem případě pythoních modulů) a skript,  který po spuštění provede všechny testy. 

Toto je příklad, který  použijeme v našem RoboProjektu:
```yml
language: python
python:
- '3.5'
- '3.6'
install:
- pip install -r requirements.txt
script:
- pytest -v
```
Po spuštění testu na [travis-ci.org](https://travis-ci.org) můžeme vidět , zda test proběhl správně, nebo jestli někde nastala chyba. Na pravé straně vidíme **My repositories**,  kde je přehled našich testů. Po rozkliknutí testu vidíme, že proběhla změna např. na větvi **master**, kdo změnu vytvořil, jak dlouho test trval, kdy byl vytvořen atd. Když máme test ve více verzích apod., tak se nám zobrazí **Build jobs**, kde vybereme pro nás vhodný výběr např. verze Pythonu. Poté máme k dispozici také **Job log**, který vygeneruje x řádků s tím, že většina jich je servisních, v první části vidíme server, kde byl test spuštěn, pak klon kódu z GitHub-u a instrukce které jsou dány ze souboru '.travis.yml'. V další části už je test, kde vidíme, zda test prošel (s chybou 0) a jak dlouho trval, nebo se zobrazí chyba.

Postup pro spuštění Travis CI je tedy:

 - jdeme na [travis-ci.org](https://travis-ci.org)
 - přihlásíme se přes [GitHub](https://github.com)
 - zapneme webhook pro repozitář (tím zapneme integraci mezi GitHub-em a Travis CI), nebo proběhne automaticky
 - teď kliknout na tlačítko Aktivace a vybereme repozitáře z GitHub-u, které chceme používat s Travis CI
 - přidáme soubor `.travis.yml` do git-u, dáme commit a push 
 - zkontrolujeme na Travis CI stav

Testy, které proběhly,  můžeme vidět na GitHub-u v seznamu commitů. Když někdo udělá Pull Request, tak jde vidět, jestli testy procházejí správně nebo ne.


