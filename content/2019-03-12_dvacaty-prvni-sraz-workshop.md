Title: Dvacátý první sraz - AsyncIO a WebSockets
Date: 2019-03-12 17:00:00
Modified: 2019-03-12 17:00:00
Author: Anežka Müller

Dnešní sraz byl malinko nestandardní. Protože jsme se v projektu posunuly do fáze, kdy už by bylo dobré začít pracovat na spojení jednotlivých částí naší hry dohromady a zařídit, aby mezi sebou komunikovaly, rozhod se Petr udělat pro nás workshop zaměřený na __asynchronní programování__ a __WebSockets__. Protože jsou to témata, která nemusí být zajímavá jen pro nás z RoboProjektu, otevřel workshop i pro další zájemce a sešli jsme se všichni tentokrát v Red Hatu, abychom měli dostatek místa. 

V rámci čtyřhodinového setkání jsme si nejprve vysvětlili a na jednoduchém příkladu ukázali, co to znamená asynchronní programování a k čemu je dobré. Podívali jsme se blíže na knihovnu [AsyncIO](https://docs.python.org/3/library/asyncio.html), která umožňuje napsat kód tak, aby počítač dělal více věcí zároveň, respektive zařídit, aby během toho, kdy u jednoho úkolu počítač na něco čeká, pracoval na něčem jiném. Vysvětlili jsme si základní principy, jak s touto knihovnou pracovat, a zkusili i nějaké malé praktické ukázky. 
Pro ty, koho by téma zajímalo hlouběji, k AsyncIO jsou dostupné podrobně zpracované materiály na stránkách [Nauč se Python](https://naucse.python.cz/lessons/intro/async/). 
Petr také bude mít na letošním [PyCon CZ](https://cz.pycon.org/2019/) přednášku o tom, jak vypadá AsyncIO uvnitř, jak uvnitř funguje. 

V druhé části workshopu jsme se zaměřili na WebSockets, což je protokol, který umožňuje  nepřetržitou obousměrnou komunikaci mezi serverem a klientem na portu HTTP. Použili jsme knihovnu [aiohttp](https://aiohttp.readthedocs.io/en/stable/), která umí pracovat s HTTP a WebSockets v rámci asynchronního paradigmatu, kterému jsme se věnovali v předchozí části. Pomocí této knihovny jsme si vytvořili jednoduchý server a klienta a nastavili mezi nimi vzájemnou komunikaci. Podklady k této části workshopu jsou dostupné na [GithHubu](https://github.com/encukou/ws-chat) a v dokumentaci aiohttp najdeme i jednoduché návody na to, jak vytvořit [server](https://docs.aiohttp.org/en/v3.0.1/web.html) i [klienta](https://docs.aiohttp.org/en/v3.0.1/client.html#aiohttp-client).

Záznam celého workshopu najdete zde:
<iframe width="640" height="360" src="https://www.youtube.com/embed/0EdYPukCQHg" frameborder="0" autoplay; encrypted-media; picture-in-picture" allowfullscreen></iframe>
