Title: Dvacátý druhý sraz - Mravenčí práce s kódem
Date: 2019-03-20 18:00:00
Modified: 2019-03-20 18:00:00
Author: Anežka Müller

Na začátku srazu jsme opět řešily, co se událo od posledně. 
Náš kód se hodně rozrostl a je čím dál složitější a propletenější. Při úpravách kódu se může snadno stát, že optimalizací chování nějaké části rozbijeme část jinou. 
Například dnes jsme se dostaly do situace, kdy jednoduchá úprava toho, jakým způsobem říkáme robotovi, kam se má ve fázi pohybu dál posunout, najednou generuje chybu na úplně jiném místě. Ukázalo se, že úpravou metody, která řeší pohyb robotů po herním plánu, jsme se dostaly do situace, kdy není ošetřeno, co se stane, pokud během jakéhokoliv pohybu robot spadne do díry nebo se ocitne jiným způsobem mimo herní plochu. Aktuální kód operuje s koordináty všech robotů, které se však dané situaci mění na `None` - tato hodnota pak nelze rozdělit na čísla, se kterými by se dalo dále počítat. Jako v podobných situacích podrobný rozbor chyby přímo nabízí řešení - potřebujeme se dostat do situace, aby se pohyb robota ukončil, pokud se během pohybu ocitne mimo herní plochu. 
Právě vzhledem ke zvyšující se složitosti kódu a obtížnějších částí hry, které ještě nemáme zpracované, se potřebujeme naučit, jak si práci co nejvíce zjednodušit. 

**Návrh a analýza algoritmů**

Poměrně komplexní část hry, která je ještě před námi, jsou pohyblivé pásy, které mají mnoho různých atributů a mohou ovlivňovat robota několika různými způsoby. V případě takovýchto složitějších problémů přichází ke slovu __návrh algoritmů__, kdy víme, čeho chceme dosáhnout, ale je třeba to přesně napsat. Je tedy dobré rozepsat si vše do postupných kroků, kde ošetříme všechny možné varianty toho, pokud se robot ocitne na pohyblivém pásu. Jak by měly jednotlivé kroky vypadat a jak na sebe budou navazovat.

<iframe width="640" height="360" src="https://www.youtube.com/embed/cDA3_5982h8" frameborder="0" autoplay; encrypted-media; picture-in-picture" allowfullscreen></iframe>

Jak je vidět na příkladu z videa, je to spousta mravenčí práce, protože je potřeba vše opravdu rozebrat do nejmenších detailů a co nejpodrobnějších kroků pokrývajících všechny možnosti. 
S tím pak souvisí __analýza algoritmů__, při které si postupně probereme celý postup krok po kroku a podíváme se, jestli někdy skončí. To nám pomůže odhalit situace, které nejsou správně ošetřeny a mohly by generovat problém. Pak se můžeme vrátit zpět k návrhu a dle nalezených problematických částí jej upravit.

**Řídit Roboprojekt jako projekt**

Zatím jsme v rámci práce na Roboprojektu celkem hojně využívaly na GitHubu `Issues`, u kterých je ale třeba si je rozkliknout a přečíst komentáře, aby člověk zjistil v jakém jsou stavu. To není úplně optimální, zvláště při našem počtu otevřených Issues. GitHub ale nabízí také možnost vytvořit `Project` a v něm udělat [Kanban board](https://kanbanize.com/kanban-resources/getting-started/what-is-kanban-board/), kde bude přímo vidět, v jakém stavu je která Issue a jaký je progres. 
