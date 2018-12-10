Title: Desátý sraz - testy a bity
Date: 2018-12-05 10:17:00
Modified: 2018-12-05 10:17:00
Author: Karolina Surma


# Úvod

Po období zvýšené projektové aktivity jsme se trochu nechaly ovlivnit počasím a přestaly sypat pull requesty jeden za druhým. Další sraz proto Terka začala krátkým zjišťovacím kolečkem, když jsme řekly, na čem jsme pracovaly a co nám momentálně dělá problém. Projekt se nám poslední dobou hodně rozrostl a všechny se potýkáme s tím, že i když tušíme, jak napsat novou vlastnost, vplést ji do stávajícího kódu je o dost těžší, než bylo na začátku. 
Daly jsme se na rekapitulaci otevřených pull requestů na témata:
- přidat načítání map jiné velikosti, než 12x12,
- přidat třídu Rotace (přejmenovaná na Směr - Direction) - podrobně popsaná [zde](https://roboprojekt.pyladies.cz/par-slov-o-datovem-typu-enum),
- napsat testy k jednotlivým funkcím v modulu backend,

kde jsme dospěly k závěru, že cítíme blok k recenzování kódu kolegyň, když jsou změny složitější a nedokážeme vyhodnotit, zda použité metody jsou skutečně na správném místě. Zjistit, že program pořád funguje, není těžké. Vyhodnotit, zda změny dávají smysl v kontextu celého projektu - je. 


# K čemu vlastně potřebujeme testy?

Při procházení otevřených PR jsme se chvíli zdržely u tématu testování. Nejdřív jsme dostaly za úkol dopsat testy do každé funkce modulu backend, ale když už byly napsané, Petr poznamenal: 

>Nestudoval jsem to detailně (to je na vás), ale všiml jsem si, že se tu přidává spousta chybějících testů, ale nemění se kód. To mi přijde trošku podezřelé.

Nám zřejmě ne ;). Na srazu jsme si proto společně dali krátký pokec, jak vypadá smysluplné testování. 
Například při tvoření nových metod většinou shora víme, čeho chceme dosáhnout:
- pokud otočím robotem, bude směřovat na správnou světovou stranu, 
- pokud vykreslím konkrétní mapu, na koordinátách (5, 5) bude skutečně v první vrstvě políčko *ground*,
- pokud postavím roboty na start, budou skutečně přiřazení na startovací políčka. 

To znamená, že společně s vývojem vznikají dobré testovací scénáře, které stojí za to rovnou dopsat do testovacího balíku. Je dobré psát testy, i když náš kód ještě nefunguje, ale již víme, jak chceme, aby se používal. Tím si při dalších krocích vývoje zlehčíme práci: testy v určitou chvíli zezelenají, díky čemuž víme, že jsme dosáhly naplánované funkčnosti a můžeme se vrhnout na integraci nového a starého kódu.

Člověk, jenž v danou chvíli přemýšlí o testech ke kódu, který byl už napsán někým jiným, může objevit nelogičnosti a najít lepší způsoby uspořádání dat. V tuto chvíli jeho úkol je tyto změny zanést i do testovaného kódu. 

Čeká nás tedy revize stávajících testů a případné úpravy. 


# Rychlý kuk na glosář pojmů

Kromě projektu na GitHubu si zvlášť udržujeme glosář pojmů s cílem sjednocení názvosloví a významu v kódu. Měl by reflektovat třídní diagram nakreslený v začátcích (česky) a stávající stav našich modulů (anglicky). Zároveň by měl poskytovat co nejpřesnější popis, co daný pojem v našem projektu znamená.
Jako příklad nám Petr uvedl pojem _tile_, jehož definice nebyla ideální. Původně jsme měly:
> _tile_ - třída definující dlaždici pomocí otočení dlaždice (‘rotation’) a cestou k souboru s obrázkem dlaždice (‘path’)

Po přepracování zní: 
> _tile_ je konkrétní efekt políčka (např laser nebo pohyblivý pás) s konkrétním směrem otočení. Na jednom políčku mapy může být víc těchto efektů políčka. 

Další úkol je zapracovat na glosáři, aby definice co nejlépe odpovídaly pravdě. 


# Různé způsoby zápisu čísel

Téma poslední části srazu bylo mnou objednáno již před nějakou dobou. Do kódu jsme si přidaly po třetím srazu "magické formulky": 

```python
>>>cislo = 2684354562
>>>hex(cislo)
'0xa0000002'
>>>cislo & 0xFFFFFFF # kouzelná formulka pro zjištění ID dlaždice
2
>>>cislo>>(4*7) # kouzelná formulka pro zjištění otočení
10
```

Při pokusu o napsání testu na tuto část jsem zjistila, že když formulce nerozumím, nedokážu ani jednou větou popsat, co se v ní odehrává.
Petr nám proto zařádil malé vyprávění o bitových operacích a číselných soustavách.

Začalo to číslem _tři_. Číslo je _něco_, co můžeme _nějak_ zapsat. Konkrétně trojku můžeme ukázat na prstech, napsat tři čárky, nebo použít arabskou číslici: 3. V každém z těchto případů se bavíme o stejné myšlenkové reprezentaci počtu. 
V běžném životě používáme desítkovou soustavu, což znamená, že pokud před číslo 0 dáme na začátek 1, navýšily jsme ho o deset. Pokud přidáme další 1 před 10, navýšily jsme ho o deset desítek (sto), atd. Každé další číslo je další mocnina desítky. 

Počítače zase používají dvojkovou, neboli binární soustavu. Počítač zná dva stavy: buď něco (např. magnet, světlo, napětí) je, nebo není. K tomu mu stačí jen dva symboly: 0 a 1. Každé nové číslo postavené na začátek je další mocnina dvojky.

Python umí pracovat s čísly zapsanými různými způsoby. Např. binární soustavu pozná podle `0b` na začátku výrazu. Pořád se ale jedná o stejnou hodnotu, porovnání stejných čísel ve dvojkové a desítkové soustavě je tedy vždy pravda.

```python
>>> 0b010110 
22
>>> 10+12 
22
>>> 10+12 == 0b010110
True
>>> bin(22)
'0b010110'
```

Počítače ukládají informace na určitých místech v paměti. Známe pojmy bit a bajt, kde bit je jeden takový znak (0 nebo 1), bajt - 8 znaků. V jednom bajtu, na osmi místech, můžeme zakódovat až 256 čísel (2<sup>8</sup>). 

```python
>>> 0b11111111     # maximální možná hodnota
255
```

Spousta věcí se dá zakódovat do 256 znaků. Podívejme se na znaky anglické abecedy, tzv. kódování ASCII: 6 bitů potřebuje na malou abecedu plus nějaké znaky kolem (čísla, závorky atd.), 1 bit pro zjištění, jestli písmenko je malé, nebo velké. 7 bitů stačí pro zapsání v podstatě celé standardní klávesnice, jak ji známe.

Už 4 bajty jsou dostačující třeba na to, aby reprezentovaly barvu: červenou (R), zelenou (G) a modrou (B). Každá složka je osmibitové číslo (tedy 0 až 255), které tak nějak odpovídá tomu, kolik barev je schopné rozeznat lidské oko. Čtvrtý bajt se aktuálně nejvíc používá pro označení průhlednosti. 
32 bitů je ale spousta jedniček a nul. Zde nám přichází vhod jiná soustava, postavená na šestnáctkách (2<sup>4</sup>). Jeden znak obsahuje stejnou informaci, jako 4 bity, s čímž se dá dobře pracovat. 

Pokud symboly `10` v hexadecimální soustavě znamenají `16` v desítkové, jak vyjádřit číslo 15? Šestnáctková soustava používá čísla 0-9 a dál: A, B, C, D, E, F. 

```python
>>> 0x10
16
>>> hex(16)
0x10
>>> 0xF
15
```

Kódy barev můžeme tedy buď uvádět v rozsahu 0-255 pro každou barevnou složku, nebo v hexadecimální soustavě, kde na dvou místech máme červenou, na dvou zelenou, na dvou modrou a na dvou posledních - průhlednost. 

A zde, u hexadecimální soustavy, se dostáváme k programu Tiled a způsobu, jakým zapisuje čísla. Používá totiž čtveřice bajtů na reprezentaci políčka ve vrstvě mapy: tři jsou číslo dlaždice, a jeden - rotace. 

Pokud si testovací dlaždici uložíme ve čtyřech různých směrech a podíváme na čísla, které nám uvede Tiled po exportu mapy do JSONu, budou vypadat pro lidské oko dost šíleně. Pokud je ovšem převedeme do hexadecimální soustavy, začnou dávat trochu smysl:

```python
>>>cisla = 49, 2684354609, 3221225521, 16160612785
>>>[hex(c) for c in cisla]
['0x31', '0xa0000031', '0xc0000031', '0x60000031']
```

`000031` je číslo naši dlaždice, její ID (ony tři vyhrazené bajty)
`00`, `a0'` `c0`, `60` je bajt s otočením. Jednotlivé bity skrývající se pod tímto označením mají speciální význam: jeden bit je na otočení ve vertikální ose, druhý - horizontální, třetí - transpozice. 

Existují způsoby, jak vzít konkrétní bity z nějakého čísla, slouží k tomu bitový operátor `&` (AND). Mezi oběma čísly nad každým bitem proběhne logické vyhodnocení pravda/nepravda, které se promítne do výsledku: 
- `1` neboli _pravda_ je pouze tam, kde na obou místech porovnávaných čísel byla jednička.
- `0` neboli _nepravda_ pro všechny ostatní případy. 
Jinými slovy, pokud v naší porovnávací operaci uvedeme na některé místo nulu, zaručíme si tím, že výsledek bude vyhodnocen jako nepravda.

Pokud vím, že informace o rotaci dlaždice je na dvou prvních místech, můžu si nadefinovat takovou operaci, která mi vrátí pouze první číslice, zbytek ignoruje:
```python
>>> hex(0x12345678 & 0xff000000)
'0x12000000'
```

Další věc, kterou s ním můžu udělat, je posunout si bity na některou stranu pomocí operátoru `<<` nebo `>>`. Pokud mě skutečně zajímají jen dvě první číslice, odstraním zbytek tak, že posunu výraz o 3 krát 8 bitů:

```python
>>> hex((0x12345678 & 0xff000000) >> (3*8))
0x12
```
Byla to fascinující odbočka od Pythonu, ale musím říct, že mi magie teď nepřipadá ani o kousek méně magická :). 

