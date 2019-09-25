Title: Hlavní téma - síť
Date: 2019-07-16 15:32:00
Modified: 2019-07-17 15:32:00
Author: Karolina Surma


## Tip na Markdown

Sraz začal výjimečně připomínkou k formátování zpráv na blogu.
Máme tendenci psát dlouhé odstavce, se kterými si git a GitHub neví dobře rady.
Když něco v textu, který se táhne na několik řádků, změníme, GitHub už neoznačí konkrétní změnu, ale pro jistotu podsvítí celý ten řádek. 
Je proto lepší texty psát tak, ze každá věta bude na jednom řádku. 
Čtenář blogu si toho nevšimne, protože na stránkách se vše poskládá dobře, a my máme nástroj, jak kontrolovat i drobné změny textu.


## Úprava interface: nechceme pořád posílat zprávy serveru

Máme s interface problém: pořád posílá serveru zprávy. 
I když hráč potvrdí svůj výběr, při každém zmáčknutí jakékoli klávesy posílá serveru zprávu se svým stavem. 
To se nám nelíbí a chceme to změnit. 
Zde ale přichází na řadu aspekt, o němž jsme doposud vůbec neuvažovaly, a to bezpečnost síťové komunikace.
U komunikace server - klient chceme, aby server byl náš zdroj pravdy a byl ten prvek, který "šéfuje" všechno, co se k němu dostane. 
Můžeme si představit, že se k našemu pythonnímu serveru někdo bude chtít napsat jiného klienta (třeba v jiném programovacím jazyce, např. webového v JavaScriptu nebo ovladače robotů z 3D tiskárny).
Kdyby k tomu někdo napsal falešného klienta, který umí vyměnit karty za jiné, pozměnit nějaké atributy hry, nebo poslat přímo škodlivé zprávy, náš server musí vědět, že na takovou zprávu nemá reagovat. 
Pokud zpráva od klienta nebude dávat smysl, je lepší ji ošetřit na straně serveru. 
Takže náš problém není ve skutečnosti, že chceme přestat posílat zprávy z klienta, ale v tom, že server už nemá v jisté chvíli zprávy přijímat. 
Vycházíme z předpokladu, že klient nám může poslat cokoliv. 
Jakmile klient pošle informaci, že potvrdil výběr, ignorujeme další zprávy.


## Jak zahrát hru?

Zprovozňujeme hru podle nástřelu serveru, který jsme společně vypracovaly minule. 
S každým novým krokem vidíme, co všechno ještě není dotažené, a snažíme se to propojit. 
Úpravy kódu potřebné pro to, aby každý robot hrál své karty a interface se pročistil po každém kole, trvaly téměř celý dnešní sraz.
Už opět vidíme, proč je dobré si namyslet algoritmus dopředu.
Potýkáme se čím dál víc s tím, že je náš kód už hodně složitý, měly bychom se proto zamyslet, jak ho zjednodušit a zdokumentovat. 

## Projekte, spusť se sám

Během analýzy, jak spustit funkční hru, jsme téměř hodinu spouštěly: v jednom terminálu server, ve druhém receiver (obecenstvo), ve třetím interface, ve čtvrtém druhý interface (simulace hry dvou hráčů). 
Je to úmorné, pokud to člověk musí dělat pořád dokola. 
A jako všechno, i to lze trochu usnadnit. Klienty můžeme přepsat do importovatelné podoby. 
Importovatelná podoba je taková, která nevyvolává vedlejší efekty. Pythonní soubory se čtou řádek po řádku a příkazy provádí i při importu do jiného modulu. 
Je proto zvykem ty příkazy, které vyvolávají vedlejší efekty, jako u nás spuštění webové aplikace nebo `ensure_future` od _asyncio_, zařádit do funkce `main()`. 
Pak s kouzelným řádkem `if __name__ == "__main__":` můžeme modul bez potíží naimportovat do spouštěcího skriptu.

Náš spouštěcí modul bude mít tedy naimportované moduly: `client_receiver`, `client_interface` a spustíme jejich `.main()` tolikrát, kolik chceme jednotlivých instancí. 
U nás je to jednou receiver a dvakrát interface.
Aby se nám vykreslila okénka, naimportujeme k tomu Pyglet a spustíme pygletí aplikaci.

Co takto nejde ještě spustit, je server. 
Musely bychom se podívat do dokumentace _aiohttp_ nebo zamyslet nad vlákny, abychom ho zprovoznily.
Zatím to tak necháme - redukce 4 terminálů do 2 je pořád pěkná časová úspora :).


## Vytvoření třídy `Server()`

Minule jsme předělaly naše [klienty na třídy](https://roboprojekt.pyladies.cz/vyvijime-rozhrani), jejichž instance vytváříme pro spuštění hry.
Chtěly jsme podobně přepsat server, který je momentálně shlukem neprovázaných funkcí.
Zde jsme narazily na problém s dekorátorem `@routes.get`, který po přepsání serveru přestal fungovat.
Je to kus kódu, který zajišťuje, že se každý druh klienta připojí k metodě, která mu poskytne to, co potřebuje k vykreslení své části hry. 
Každá "routa" má tedy nadefinovaný řetězec, kterým se obě strany propojí.
Python nejprve čte "recept" na vytvoření třídy `Server` a až potom vytváří jeho konkrétní instanci. 
Při čtení receptu ještě ale žádné `routes` nejsou (neexistuje konkrétní instance), a tak nám při použití `@routes.get` Python vynadá a nepovolí server pustit.

Musíme ten kus kódu tedy rozepsat. 
Podíváme se na dokumentaci k `aiohttp.web.Application().add_routes()`.
Podle kapitoly [Resources and Routes](https://docs.aiohttp.org/en/latest/web_quickstart.html#resources-and-routes) předěláme naše _routy_ přímo do aplikace mimo samotnou třídu `Server`. 

```python
def get_app(argv=None):
    app = web.Application()
    app.add_routes(
        [
            web.get("/receiver/", server.receiver),
            web.get("/interface/", server.interface),
        ]
    )
    return app
```
