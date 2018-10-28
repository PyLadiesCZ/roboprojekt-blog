# Blog RoboProjektu

Tento blog je vidět na adrese [pyladiescz.github.io/roboprojekt-blog](https://pyladiescz.github.io/roboprojekt-blog).

## Jak přispívat

### Lokální instalace

Nainstaluj si `pipenv`, jestli ho ještě nemáš:
```
$ pip install --user pipenv
```
(Případně do virtuálního prostředí bez `--user`.)

Vytvoř si na počítači projektový adresář, blog si naklonuj k sobě a nainstaluj závislosti:

```console
$ git clone https://github.com/PyLadiesCZ/roboprojekt-blog
$ cd roboprojekt-blog
$ pipenv install
```
### Lokální spuštění
Po nainstalování blog „spusť“; otevře se v prohlížeči:
```console
$ pipenv run preview
```
### Přidání článku
Článek se přidá pomocí:
```
$ pipenv run write
```
To se tě zeptá na pár informací a otevře (nějaký) editor.
Nebo místo toho můžeš rovnou zkopírovat a upravit existující článek z adresáře `content`.

### Markdown

Články jsou psány v jazyce [Markdown](https://guides.github.com/pdfs/markdown-cheatsheet-online.pdf), který využiješ napš. v komentářích na GitHubu, buňkách Jupyter Notebooku, materiálech pro naucse a podobně. Na rozdíl od programů jako Word se formátovací instrukce (např. „tučné písmo“) píše přímo do textu.

Markdown můžeš psát ve svém editoru, nebo v [některé z webových aplikací](https://stackedit.io/app) které to zjednodušují, a pak to do edirtoru zkopírovat.

Základy Markdownu:

* Nadpisy piš na samostatný řádek a dej před ně `#`, `##`, `###` … podle důležitosti nadpisu
* Odstavce odděluj prázdným řádkem
* *Zvýraznění* se dělá hvězdičkama: `*zvýraznění*` nebo podtržítkama: `_zvýraznění_`
* Pro **silnější** __zvýraznění__  hvězdičky zdvoj: `**silnější** __zvýraznění__`
* Malé kousky kódu, jména proměnných, příkazy do řádky atp. obal do „obrácených čárek“:
  ```markdown
  Metoda `__init__` je speciální.
  ```
* Větší kousky kódu obal do trojitých „obrácených čárek“; za první z nich uveď jméno jazyka:

      ```python
      def add(a, b):
          return a + b
      ```
* Text odkazů obal do hranatých závorek; hned za ně dej URL v kulatých: `[Tahák na Markdown](https://guides.github.com/pdfs/markdown-cheatsheet-online.pdf)`.
* Obrázky můžeš nahrát lokálně do adresáře content/images použitím následující syntaxe: `![Popisek](./images/obrazek.jpg)`

Víc najdeš v [taháku](https://guides.github.com/pdfs/markdown-cheatsheet-online.pdf) od GitHubu.

### Přidávání článku

Až článek dopíšeš, ujisti se, že máš správně nakonfigurovaný git (podle sekce: Posílání změn popsané na [stránkách naucse.cz](https://naucse.python.cz/2018/pyladies-brno-podzim/git/collaboration/))
Pokud nemáš uložen odkaz na svůj repozitář, přidej si ho pomocí `git remote add`, jak je popsáno v odkaze výše.

Pro přidání článku ho pošli do Gitu (známou dvojicí *git add*, *git commit*), a následně pošli do **svého** (osforkovaného dle návodu výše) GitHubového repozitáře pomocí příkazu `git push tvojejmeno master`. 

Na stránkách GitHub.com své změny pošli jako Pull Request na /PyLadiesCZ/robotprojekt-blog.
