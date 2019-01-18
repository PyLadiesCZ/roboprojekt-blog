Title: �trn�ct� sraz � opakov�n� a vysv�tlov�n�
Date: 2019-01-15 08:39:00
Modified: 2019-01-15 08:39:00
Author: Iveta �esalov�



Tento t�den jsme se se�ly v komorn�m po�tu, nav�c bez Petra. Ale c�l srazu byl jasn� � abychom v�echny rozum�ly st�vaj�c�mu k�du.
Za�aly jsme souborem *util.py* a proch�zeli metodu po metod� jednotliv�ch t��d. V�niv� diskuze nastala u t��dy HoleTile, kter� vol� metodu robota � robot.die(). P�vodn� bylo v k�du naps�no, �e si robot volal metodu d�ry, co� Petrovi p�i�lo zvl�tn� :-) Nyn� je to tedy metoda pol��ka vyvol� metodu robota, co� je logi�t�j��, ne� aby si robot vyvolal metodu pol��ka :-D

```python
class HoleTile(Tile):
    def kill_robot(self, robot):
        # Call robot's method for dying
        return robot.die()
```

Byla to dlouh� hodina, ale smyslupln�. Potom jsme se p�esunuly k souboru *backend.py* a n�sledovalo dal�� vysv�tlov�n�, co� souviselo s op�tovn�m prob�r�n�m pravidel hry.
Pokud robot um�e, p�i�ad� se mu sou�adnice [-1, -1], aby byl tedy mimo hrac� plochu. Narazily jsme ov�em na probl�m, �e kdy� robot o�ije, nem��ou se zobrazit dva roboti na sob�, pokud na jeho startovn�m pol��ku stoj� jin� robot. Bude nutno se zamyslet, jak to vy�e�it, jestli zobrazen�m dal��ho ok�nka, kter� se hr��e zept�, kam chce robota um�stit, nebo n�hodn� rozm�st�n� na voln� startovn� pol��ko�

Dal��m t�matem bylo Rozhran�, aneb pull request s n�kolika stovkami ��dk�. Pro p�ehlednost jsme narazily na jednu vychyt�vku, pokud se na githubu m�n� velk� mno�stv� soubor�, sta�� zm��knout `alt` a kliknout na �ipku a v�echno se sroluje a sn�ze najdeme soubor, kter� pot�ebujeme.

 ![github](./images/github.jpg


Pro�ly jsme k�d a uk�zaly jsme si, co v�echno funguje, jak u� obrazovka reaguje na r�zn� kl�vesy atd. Trochu jsme se pozastavily nad bal��kem karet. Budeme poka�d� rozd�vat z nov�ho, stejn�ho bal��ku karet, kter� se zam�ch� a nebudou se tam vracet rozdan�, kter� si hr�� nevybere.

P��t� se sejdeme ji� v pln�m po�tu a ur�it� n�s Petr nakopne spr�vn�m sm�rem, jak d�le pokra�ovat :-)