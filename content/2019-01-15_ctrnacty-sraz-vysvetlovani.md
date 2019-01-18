Title: Ètrnáctý sraz – opakování a vysvìtlování
Date: 2019-01-15 08:39:00
Modified: 2019-01-15 08:39:00
Author: Iveta Èesalová



Tento týden jsme se sešly v komorním poètu, navíc bez Petra. Ale cíl srazu byl jasný – abychom všechny rozumìly stávajícímu kódu.
Zaèaly jsme souborem *util.py* a procházeli metodu po metodì jednotlivých tøíd. Vášnivá diskuze nastala u tøídy HoleTile, která volá metodu robota – robot.die(). Pùvodnì bylo v kódu napsáno, že si robot volal metodu díry, což Petrovi pøišlo zvláštní :-) Nyní je to tedy metoda políèka vyvolá metodu robota, což je logiètìjší, než aby si robot vyvolal metodu políèka :-D

```python
class HoleTile(Tile):
    def kill_robot(self, robot):
        # Call robot's method for dying
        return robot.die()
```

Byla to dlouhá hodina, ale smysluplná. Potom jsme se pøesunuly k souboru *backend.py* a následovalo další vysvìtlování, což souviselo s opìtovným probíráním pravidel hry.
Pokud robot umøe, pøiøadí se mu souøadnice [-1, -1], aby byl tedy mimo hrací plochu. Narazily jsme ovšem na problém, že když robot ožije, nemùžou se zobrazit dva roboti na sobì, pokud na jeho startovním políèku stojí jiný robot. Bude nutno se zamyslet, jak to vyøešit, jestli zobrazením dalšího okýnka, které se hráèe zeptá, kam chce robota umístit, nebo náhodné rozmístìní na volné startovní políèko…

Dalším tématem bylo Rozhraní, aneb pull request s nìkolika stovkami øádkù. Pro pøehlednost jsme narazily na jednu vychytávku, pokud se na githubu mìní velké množství souborù, staèí zmáèknout `alt` a kliknout na šipku a všechno se sroluje a snáze najdeme soubor, který potøebujeme.

 ![github](./images/github.jpg


Prošly jsme kód a ukázaly jsme si, co všechno funguje, jak už obrazovka reaguje na rùzné klávesy atd. Trochu jsme se pozastavily nad balíèkem karet. Budeme pokaždé rozdávat z nového, stejného balíèku karet, který se zamíchá a nebudou se tam vracet rozdané, které si hráè nevybere.

Pøíštì se sejdeme již v plném poètu a urèitì nás Petr nakopne správným smìrem, jak dále pokraèovat :-)