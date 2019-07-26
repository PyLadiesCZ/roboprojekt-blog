Title: Co dělá server: zprávy, context manager a jak porovnávat hodnoty v Pythonu
Date: 2019-06-11 18:00:00
Modified: 2019-06-11 20:00:00
Author: Karolina Surma

## is vs ==

`==` je porovnání, které ověří hodnotu objektů, které jsou porovnávány.

```python
>>> 1.0 == 1
True
>>> 1.0 == True
True
```

U každého datového typu můžeme upravit chování porovnávání přepsáním speciální metody `__eq__`. Psaly jsme o tom post [zde](https://roboprojekt.pyladies.cz/dvacaty-sraz-testy).

A `is` vyhodnotí, jestli je to tentýž, stejný objekt.
Příklad níže se vyhodnotí jako nepravda, protože dva prázdné seznamy jsou dva různé objekty.

```python
>>> [] is []
False
```

Dva prázdné seznamy se sice rovnají, pokud je vyhodnotíme pomocí `==`, ale v budoucnosti tomu tak nemusí být:

```python
>>> a = []
>>> b = []
>>> a == b
True
>>> a.append(1)
>>> a == b
False
```

Zatímco `is` kontroluje, že je to úplně přesně to samé. 

```python
>>> 1.0 is 1
False
>>> 1 is 1 
True
```

U posledního příkladu vzniká problém, protože u celých čísel se Python chová trochu nestandardně: nezáleží mu, jestli jde o tentýž objekt, nebo jiný objekt s hodnotou čísla 1.
Navíc malá a velká čísla se chovají trochu jinak:

```python
>>> a = 1
>>> b = 1
>>> a is b
True

>>> a = 1000
>>> b = 1000
>>> a is b
False
```

U některých objektů proto `is` může být zrádné. U `True`, `False` a `None` tento problém není, protože nemůžeme vytvořit další objekt "True", vždy se jedná o stejnou instanci logické hodnoty.
Když chceme použit vyhodnocení atributu s _bool_ hodnotou v podmínce, neměly bychom ale používat ani `==`, ani `is` - správný způsob, jak takovou podmínku napsat, je:

```python
if atribut: # místo "if atribut is True"
    print("Ha!")
if not atribut: # místo "if atribut is False"
    print("Nene!")
```

U `None` je situace trochu jiná, zde opravdu chceme zjišťovat, jestli hodnotou atributu je `None`, nebo ne, takže:

```python
if atribut is None:
    print("Jsem prázdný")
if atribut is not None:
    print("Nejsem prázdný")
```

`is` je trochu rychlejší a vyhodnocení podmínky tak trvá o něco méně, než v případě tradičního porovnávání.
Jako zajímavost jsme se dozvěděly, že o `is` a `==` se točí v pythonním světě diskuze, a dokonce autor Pythonu, Guido, se vyjádřil pro sjednocení porovnávání ve prospěch `==`. 
Není to totiž triviální a začátečníci mívají problém s uchopením, kdy používat který způsob.


## Třídy, víc tříd!

Naši klienti používají čím dál víc globálních proměnných. Některé věci, jako např. pygletí okno s hracím rozhraním, nastavujeme na začátku na `None` a plníme je postupně díky zprávám od serveru.
Už bychom se měly zamyslet, jak klienty přepsat na třídy, kde tyto globální proměnné převedeme na atributy třídy, které budou k dispozici pro všechny metody. 
Na názorné ukázce jsme se přesvědčily, že přepsání není hodně složité: atributy se přenesou do metody `__init__`, jako _self.atributy_, metodám dáme `self` jako první argument a předěláme bývalé globální proměnné v jejich tělech. 
Další výhoda třídy oproti kódu, který doposud máme, je jednoduchost importování. 
Můžeme takovou třídu `Interface()` naimportovat do jiného programu, např. nové hry, a budeme mít přístup ke všem jejím metodám pomocí jednoho řádku kódu: `from interface import Interface`.


## Dva klienti - jeden server

V další části srazu jsme se podívali na _draft Pull Requestu_. 
Během našeho psaní Roboprojektu Github přišel se zajímavou funkcí - nyní při vytváření PR můžu vybrat, jestli chci zpřístupnit svůj PR pro začlenění (považuji ho za finální), nebo na něm chci ještě pracovat (a merge není povolen).

![draft](./images/draft.JPG)

Potřebujeme donutit náš server, aby mluvil i s klientem, který vykresluje hrací plochu, i s hráčem. 
Každému posílá společný stav hry, ale hráči pošle dodatečně informace o jeho robotovi a karty. 
Hráč serveru navíc odpovídá zprávami s obsahem karet nebo o tom, zda hraje další kolo.
Potřebujeme tedy rozlišit, aby server posílal každému jen informace, které mu patří. 
No a jak se klienti při připojení "představí"? Vyřešily jsme to pomocí `route` dekorátoru, který určuje, na jaké adrese budou spolu komunikovat server s klientem. 
Doposud jsme tam měly: `routes.get(/ws/)` a jednu funkci, která komunikovala s klienty. Nově rozlišujeme:
```python
@routes.get(/interface/)
@routes.get(/receiver/)
```
Které dekorují zvláštní funkce: jednu pro plochu, druhou pro hráče.
Každý klient má povolenou jednu - svou - cestu. 

Je to sice čisté řešení, každý komunikuje se serverem na _svém_ kanálu, ale začal se nám opakovat kód: server musí v obou případech navázat spojení s klientem, přidat ho do seznamu klientů, a na konci bezpečně spojení ukončit vč. odstranění ze seznamu klientů. 
Chceme tak ošetřit začátek a konec funkce, zatímco vnitřek je jiný.

S pomocí nám přijde `context manager`.

## contextlib.contextmanager

Můžeme použit dekorátor z knihovny `contextlib`.
Když nějaké funkci dáme dekorátor `contextmanager`, taková funkce se může použít s příkazem `with`. Příkaz `with` už známe například z [operací na souborech](https://naucse.python.cz/course/pyladies/beginners/files/). 
Když otevřeme soubor s `with`, zajistíme si, že se v každém případě hezky uzavře, i kdyby náš program spadl v půlce běhu kvůli nějaké chybě. 
Python umožňuje nám vytvářet vlastní context managery, kterým řekneme, co mají udělat před zavoláním naši funkce a po jejím doběhnutí.
Můžeme s nimi pracovat dvěma způsoby. Buď vytvoříme třídu, která má dvě metody:
```python
>>> class Kontext:
>>>     def __enter__(self):
>>>         print("zacatek")
>>>         return 'NECO'
>>>     def __exit__(self, *args):
>>>         print("konec")
>>>         
>>> with Kontext() as neco:
>>>     print(neco)
zacatek
NECO
konec
```
Na začátku se provede metoda `__enter__`, a na konci `with` bloku se provede `__exit__`.
Důležité je, že i když uděláme chybu uprostřed své funkce, konec se vždy zavolá a vyčistí po nás prostředí. 
Další věc, kterou umí dělat kontext manager, je to, že dokáže naši chybu chytit a předat ji nám na další zpracování.
```python
>>> class Kontext:
>>>     def __enter__(self):
>>>         print("zacatek")
>>>         return 'NECO'
>>>     def __exit__(self, _a, exc, _b):
>>>         print("konec", repr(exc))
>>>         
>>> with Kontext() as neco:
>>>     print(neco)
>>>     raise RuntimeError()
```

výsledek bude: 
```python
zacatek
NECO
konec RuntimeError()
```

Toto např. dělá `with pytest.raises`, o němž jsme se učily [v začátečnickém kurzu](https://naucse.python.cz/course/pyladies/beginners/testing/) - podívá se, jestli chyba, která vznikla, je chyba, kterou očekáváme. Pokud ano - test prochází, pokud ne - Pytest vyvolá vlastní chybu a řekne nám o tom.

Problém tohoto přístupu je, že je... dlouhý. Zde přichází na pomoc Pythonní `yield`. 
Můžeme si napsat context manager, který udělá totéž jako naše třída výše.

```python
>>> @contextlib.contextmanager
>>> def kontext_funkce():
>>>     print("zacatek")
>>>     yield NECO
>>>     print("konec")
>>> 
>>> with kontext_funkce() as neco:
>>>     print(neco)
```    
Dekorátor je tak chytrý kus kódu, udělá všechny ty kroky za nás.
Zajímavé cvičení by bylo napsat takový context manager od začátku, my se ale spokojíme s tím, že už někdo napsal dekorátor připravený k využití.
Dokonce můžeme vylepšit náš context manager a přidat odchycení své chyby:
```python
>>> @contextlib.contextmanager
>>> def kontext_funkce():
>>>     print("zacatek")
>>>     try:
>>>         yield NECO
>>>     except RuntimeError:
>>>         print("oops")
>>>     print("konec")
>>> 
>>> with kontext_funkce() as neco:
>>>     print(neco)
>>>     raise RuntimeError()
zacatek
NECO
oops
konec
```

Takový kontext využijeme pro náš server. Protože tvoříme hru s využitím asynchronní knihovny `asyncio`, náš context manager bude patříčně jiný: `@contextlib.asynccontextmanager`


## Zprávy server - klient

Zatím posíláme klientům zprávy jako stringy, kde prvních pár znaků je vždy stejných, např. "Robot: Bot123". Tyto zprávy máme překlopit na JSON, protože:
- jednoduše jdou překládat na Pythonní slovníky
- nemusíme je následně složitě parsovat (kdokoli se pokoušel parsovat textové zprávy, ten ví, jak to bolí)
Druhy zpráv můžeme od sebe oddělit tak, že vždy nastavíme na začátku stejný klíč, např "kind"="state", nebo "kind=robot" a podle toho naučit klienta na zprávy reagovat.

**Finální struktura serveru**

Polovinu srazu nám zabrala analýza návrhu fungování serveru. V rámci analýzy jsme se shodly na třech prvcích, ke kterým musí patřit veškerá funkčnost tohoto nástroje:
1. Server dělá něco pro klienta, který se právě k němu připojil (pošle mu robota, první stav hry, první karty etc.)
2. Server dostává zprávy od klienta a nějak s nimi nakládá (vybrané karty, nehraju dál, etc.)
3. Server posílá aktualizovaný stav hry všem připojeným klientům.

Na tomto základě postavíme celý nás server.

