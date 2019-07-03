Title: Pokračujeme se síťovou komunikací
Date: 2019-07-02 22:28:00
Modified: 2019-07-02 22:28:00
Author: Karolina Surma


Po dvoutýdenní pauze jsme se opět sešly nad komunikací server-klient. Krok po kroku připisujeme nové funkcionality. Náš server už umí poslat klientovi jemu přiřazeného robota a karty, ze kterých si klient vybírá 5 pro odehrání herního kola. Chybí nám odhazovací balíček: pokud serveru dojdou karty na rozdání dalšímu robotovi, měl by vzít všechny doposud odhozené karty a vytvořit z nich nový herní balíček. 

## Interface

Změnilo se pozadí - ve spodní části interface se nyní vykresluje tolik okének pozadí robotů, kolik bude na mapě hráčů. Ještě řešíme vykreslení avatarů samotných robotů, což určitě budeme mít před dalším srazem hotové.
Klient posílá taky serveru vybrané karty s informaci že skončil výběr a zprávu, jestli hraje toto kolo (power down). Server tyto informace umí dekódovat a přeložit na příslušné atributy stavu hry.
V dalších krocích naučíme klienta číst zprávu o stavu svého robota ze stavu hry (nyní klientovi posíláme separovaná data, aby si sám vytvořil robota).

## Jména a indikátory

Přejmenovaly jsme roboty. Doposud nesli jména osob, které je nakreslily v Inkscape'u během prvních týdnů projektu. Nyní mají opravdu kybernetická pojmenování. A zde nás, po přejmenování desítek souborů a spoustě změn v kódu, zastavil Petr. Je totiž rozdíl mezi jménem - tím, které ukazujeme hráči navenek, hezky zformátovaným, s velkými písmeny atd., a indikátorem, s nímž pracujeme uvnitř svého programu a nepropagujeme dál k uživateli. Indikátory není vhodné měnit, jsou zapletené do funkcí programů a každá jejich změna vyžaduje řetězec dalších. Naopak jména jsou čistě jen na nás - herní logika je znát nemusí, patři pouze frontendu. Je to vhodné jak pro vlastní formátovaní jmen, tak pro např. jazykové mutace. A jak dát takové jméno robotovi? Pokud má náš robot poznávací indikátor _franta_, ale přejeme si ho zobrazovat pod jménem _Roy Batty_, můžeme vytvořit soubor `yaml` s název rovným indikátoru, a do těla napsat `name: Roy Batty`. Python v našem frontendu si jméno jednoduše přečte a vykreslí. 

## Alternativní pohled na server

Petr se před několika srazy zmínil, že on by svůj server navrhl jinak. Abychom si ale užily proces vymyšlení serveru a přidávání mu nových funkcí, hned nám neřekl, jak by tyto otázky řešil on. Jelikož jsme už poměrně daleko v implementaci (konec se blíží!), dnes jsme se dozvěděly, jak bychom to mohly řešit jinak.
Pro komunikaci server - klient používáme asynchronní knihovnu AsyncIO. Ta v sobě obsahuje třídu [Queue](https://docs.python.org/3/library/asyncio-queue.html). Asynchronní fronta je z jedné strany otevřená pro vstup, z druhé strany pro výstup, což bychom mohly využít v situaci, když čekáme na informace od klientů. Server v podání Petra by měl zvlášť herní logiku a zvlášť síťovou komunikaci. Pokaždé, když by od klienta přišla nová zpráva na server (např. vybrané karty hráče), přidala by se do fronty, která by _se pošťouchla_, že může zpracovat další kus dat. Až by z fronty vypadly vybrané karty posledního hráče, provedl by se další kus herní logiky (např. herní kolo - efekty karet a políček). 

## Spojování slovníku

Nová vlastnost Pythonu - spojování slovníků. 
Když máme dva slovníky:

```python
barvy = {"zelena": "green", "cervena": "red"}
tvary = {"kruh": "circle", "ctverec": "square"}
```
můžeme je postaru spojit dohromady tak, že vytvoříme nový slovník a následně ho aktualizujeme o dva slovníky:
```python
cze_eng = {}
cze_eng.update(barvy)
cze_eng.update(tvary)

cze_eng
> {"zelena": "green", "cervena": "red", "kruh": "circle", "ctverec": "square"}
```
Nově to lze udělat rychlé a jednoduše:
```python
cze_eng = {**barvy, **tvary}
cze_eng
> {"zelena": "green", "cervena": "red", "kruh": "circle", "ctverec": "square"}
```
