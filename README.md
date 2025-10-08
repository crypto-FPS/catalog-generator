# Catalog Generator


Prosty skrypt generujący katalog produktów na podstawie pliku CSV i szablonu w formacie HTML.
Wynik: HTML i PDF z okładką, katalogiem produktów i stroną kontaktową.

## Wymagania
- Python 3.10+
- Biblioteki Python znajdujące się w requirements.txt

## Instalacja


Zainstaluj wymagane pakiety:

```bash
pip install -r requirements.txt
```


## Struktura projektu

``` 
projekt/
├── data/                  → plik CSV z produktami (products.csv)
├── templates/             → szablon HTML katalogu (catalog_template.html)
├── assets/                → okładka, strona kontaktowa, tło, czcionki
├── output/                → wygenerowane pliki HTML i PDF
├── temp_images/           → tymczasowe obrazki (czyszczone automatycznie)
├── generate_catalog.py    → główny skrypt
├── .gitignore
├── README.md
└── requirements.txt
```


## Przygotowanie programu


Foldery data/ i assets/ należy stworzyć.

Folder temp_images/ jest tworzony automatycznie.

Przed uruchomieniem należy je uzupełnić odpowiednimi plikami:
* data/ -> products.csv (z kolumnami: category,name,images 1)
* assets/ -> pliki w formacie a4: okladka.pdf, strona_kontaktowa.pdf, background.png (2480 x 3508 px); pliki czcionek: ThunderhousePro.ttf, ImFellEnglishSC.ttf

Należy zwrócić uwagę, na **dokładną nazwę plików**


## Użycie


Uruchom skrypt:
```bash
python generate_catalog.py
```


## Wynik

W folderze output/ znajdziesz pliki catalog.html (używany do generowania) i catalog.pdf (finalny produkt)
