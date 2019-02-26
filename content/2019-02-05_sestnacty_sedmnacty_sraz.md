Title: Šestnáctý a sedmnáctý sraz - co máme a funguje
Date: 2019-02-05 18:00:00
Modified: 2019-02-05 09:58:00
Author: Iveta Česalová

Tyto srazy byly opět v duchu velkého vysvětlování, co všechno již v kódu je a co funguje. Začaly jsme základními soubory jako je README.md a narazily na malé nedostatky. Je nutno doplnit informaci o automatickém exportu obrázků pomocí `export_img.py`. Dále je lepší změnit `python -m pip install pyglet` na `python -m pip install -r requirements.txt`, v případě doplnění dalších potřebných programů (momentálně je v souboru requirements.txt pouze pyglet).


Hra se bude pouštět souborem `game.py`. V tomto souboru je nutno mít co nejméně kódu, který nejsme schopny testovat a bude spojovat všechny ostatní soubory dohromady. Je tam nyní pomocná funkce `def move_once(t)`, kterou je nutno odstranit. 
A narazily jsme na zásadní věc, jak vlastně hra bude fungovat, jak zadat příkazy, aby se již dalo hrát. Je nutno propojit s interface. Drobná chybička je v souboru `interface_frontend.py`, protože spouští aplikaci, což by neměl, protože jinak nepůjde importovat. Takže `window = init_window()` a `pyglet.app.run()` přesunout do `game.py`, z kterého se pustí dvě okna.


Pro zpřehlednění jsme vytvořily následující mapu, abychom věděly, která část kódu co obsahuje.

![mapa](./images/mapa.jpg)


###BACKEND.PY###
Tady jsme narazily na problém ve třídě `Robot`, kdy v ` def_walk` je problém, když robot couvá. 
```python
if distance < 0:
            self.rotate(Rotation.U_TURN)
            self.walk((-distance), state)
            self.rotate(Rotation.U_TURN)
```

V případě, že jde na sever nebo na jih, není problém. Ovšem pokud má jít na západ, je kód špatně. Je nutné ještě doplnit směr, kterým má jít.  V prvním kroku se otočí čelem vzad(`self.rotate(Rotation.U_TURN)`) tedy na jih, druhý krok popojde (`self.walk((-distance), state`) a při třetím kroku se opět otočí (`self.rotate(Rotation.U_TURN`) a kouká tedy na sever - viz obrázek. 

![posun](./images/posun.jpg)


Občas se nám objevuje duplicitní část kódu, například v metodách `def_walk`a `def_move`. Je tedy nutno vyřešit. Stejně tak máme v `def_apply_card_effect` dvakrát použitou podmínku `if_isinstance`, měli bychom na tuto část vytvořit metodu.


####Třída Robot####
V backendu ve vlastnostech robota se objevuje `self.path = path` a `self.path_front = path_front`. Jelikož se jedná o cestu k obrázkům, patří to do frontedu a pokud to chceme propojit, je vhodné místo toho robota pojmenovat.

V metodě `def_inactive(self)` jsou jako souřadnice neaktivního robota použity `(-1, -1)` . Nedávají nikdy smysl jako čísla (x, y), nutno změnit na `None`, protože robot v té chvíli není na hrací ploše.


Kód ve funkcích `def get_starting_coordinates(board)` a ` def get_robot_paths()` obsahuje načítání obrázků, což má být ve frontendu, takže vyřešit pojmenováním robotů a políček. Bylo by hezké mít soubor (json) s informacemi o robotech, kteří jsou na začátku hry na výběr a jména robotů načítat z něj. `get_robot_paths()` se změní na `get_robot_names()`.


###Třída Tile###
Třída `Tile` a všechny její podtřídy je velice obsáhlá a je v souboru `util.py`. Bylo by více než vhodné vytvořit samostatný soubor `tile.py`. 
Políčka (`Tile`) by měla jako `properties` dostat slovník jako např. `{'crossroads': True, 'direction': 90, 'count': 2}` a neměla by ignorovat jména vlastností.




###FRONTEND.PY###
Ve frontendu jsme stále nevyřešily načítání obrázků mimo funkci `def create_sprites`. Cyklus pro načítání obrázků dát na začátek kódu a v této funkci už na ně budeme odkazovat např. jménem (`tile_image`, `robot_image`). Nejtěžší bude vymyslet logiku s vracením jména.


###INTERFACE.PY###
Ve funkci `def switch_power_down` by se mohl následující kód zjednodušit.
```python
if self.indicator == False:
	if self.power_down == False:
		self.power_down = True
	else:
		self.power_down = False
```

Lze nahradit:
`self.power_down = not self.power_down`
Co dělá `not`? Když je hodnota `True`, vrátí `False` a obráceně.


Jak uvažuje programátor? :-) Když separujem backend a frontend, je dobré se zamyslet, jak by se mohl frontend napsat zcela jinak, například zcela jednoduše jen v příkazové řádce. 

![alternativni_frontend](./images/afrontend.jpg)


Nejčastější chybou v celém kódu je pojmenování proměnných, jejichž název nesouhlasí přesně s tím, co dělá kód, nebo se liší od komentářů apod.

* `tile_count` se mezi `get_start_state` a `State.__init__` přejmenuje na `sizes`
* `State.game_round` se podle pravidel řekne `register`
*  v kódu je `next_coordinates`, v komentáři "new coordinates“
* `def_walk` - proměnná `robot_in_the_way = None` – je to číslo robota, ne robot
* v `util.py`- funkce se jmenuje `select_tile`, ovšem ona ho vybere a zároveň vytvoří
* `def init_window` by se měla přejmenovat na `create_window`
* `def draw_board(state, window)` vykreslí stav, přejmenovat :-)
