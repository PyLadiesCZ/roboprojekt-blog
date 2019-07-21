Title: Vyvíjíme rozhraní
Date: 2019-06-18 16:36:00
Modified: 2019-06-18 16:36:00
Author: Karolina Surma


Naše srazy postupně získaly stálý rámec, kdy si řekneme: 
- co nového se událo na projektu za poslední období, 
- vysvětlíme případné nesrovnalosti v otevřených PR, 
- a naplánujeme, na čem budeme pracovat dál.

Jelikož už méně přednáškujeme a jsme víc soustředěné na konkrétní problémy, vyplácí se nám práce s pracovním dokumentem s agendou, kam vkládáme vše, co nás během týdne napadne a co chceme probrat s expertem.

## Server

Tento týden je naše hlavní starost komunikace server - klient.
Minule jsme si sepsaly průvodní dokument k serveru: jak chceme, aby logicky fungoval. 
Nad tímto dokumentem jsme měly doma zaiterovat a zkusit ho přepsat do Pythonu. 
Objevily jsme spoustu dotazů a opřipomínkovaly původní dokument s cílem pochopit, jak náš server bude fungovat v detailech. Už víckrát jsme totiž zjistily, že nemá smysl sedat ke kódu, dokud nevíme, **co** chceme napsat :).
Server obecně funguje tak, že: 
1) něco pošle připojenému klientovi (*stav hry, robota, karty*), 
2) čeká na data od všech klientů (*vybrané karty*), 
3) něco pošle všem klientům (aktualizovaný *stav hry*).

Náš návrh ještě není ideální: máme naplánované odeslání karet každému robotovi na začátku, čekání na data a aktualizaci stavu. Nikde ale neposíláme všem klientům nové karty, z nichž můžou vybírat. Doplnily jsme tedy návrh algoritmu. 

Dozvěděly jsme se taky, že máme v kódu chybu, o níž nevíme. 
Jedná se o čas, který potřebuje server na zpracování karet. Může se stát, že serveru dojde interní časovač, ale ještě než o tom dá vědět klientům, dostane další zprávu s aktualizovanými kartami. Protože časové okénko na výběr už je zavřené, karty se přiřadí až k dalšímu kolu. Abychom tomu zamezily, je dobré přidat do zpráv s kartami číslo herního kola. Tím si zajistíme korektní přiřazení všech zpráv.

## Kolik stavů potřebujeme? A co patří k Interface?

Nyní vytváříme stav hry a stav rozhraní. Stav hry drží informace o mapě a robotech, zatímco stav rozhraní patří konkrétnímu hráči a ukazuje detaily jeho robota + mini obrázky ostatních hráčů. 
Řešily jsme, zda klientovi, který se zabývá vykreslením rozhraní, máme posílat i celkový stav hry. Shodly jsme se, že ano, jelikož data o všech robotech musíme "vyzobat" a aktualizovat ze stavu hry.

U stavu rozhraní máme další zajímavou věc: obsah jeho atributů totiž proudí mezi serverem a klientem: informaci o zvolených kartách, stavu `power_down` a ukončení výběru posílá hráč serveru. Data o robotovi a karty, ze kterých si může hráč vybrat, posílá hráči server.
Je důležité proto odesílané zprávy pečlivě naplánovat a vždy důkladně promýšlet, která data posíláme a která přijímáme.

Když se podíváme na stávající rozhraní, vykreslujeme ho hned s příkladovým (_fake_) robotem a kartami. 
Může se však stát, že chceme vykreslit interface, ale ještě neznáme svého robota ani nemáme karty. Interface se proto musí umět vykreslit i v případě, že tyto údaje nejsou k dispozici.

Co víc, máme v souboru s rozhraním i nějaké zavolané funkce: vytváří se v něm balíček karet, karty se rozdají a vykreslí, a vytvoří i instance třídy samotného interface. Tyto exekuce v souboru s logikou chování nechceme, dělá to kód netestovatelný a začíná se nám to přít s kódem, který postupně připisujeme serveru. Logika vytváření karet, které nepatří k logice klienta, taky nepatří tomuto souboru, měla by se přenést pod stav hry.

## Klient Interface

Jelikož náš klient obsahuje v sobě už dost kódu a začaly jsme využívat globální proměnné, aby vše fungovalo, jak si představujeme, bylo nám doporučeno překlopit stávající proceduru na třídu. Globální proměnné tak překlopíme do atributů třídy, se kterými pak můžeme jednodušeji pracovat. U takového "roztřídění" kódu je velice podstatné rozmyslet si, které atributy patří nové vytvořené třídě (`self.window`, `self.state`) a které jsou dané zvenčí (v našem případě: `text` ve smyslu vstupu z klávesnice). Pak zbývá rozchodit volání metod (spousta zapomenutých `self` po cestě, které mají za výsledek `NameError`).

## Kam patří robotí program?

Petr podotkl, že seznam karet, které má robot na ruce, možná vůbec robotovi nepatří. Provedení efektů karet a políček (funkce `apply_all_effects`) by měla dostat jako argumenty roboty a říct, co s nimi má udělat. `Program` má totiž smysl tehdy, když se provádí, samotný není vlastnost robota. 
Zatím tuto změnu zavádět nebudeme, ale je dobré si na ní pamatovat do budoucna, až budeme mít chuť něco refaktorovat :)
