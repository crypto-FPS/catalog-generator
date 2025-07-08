# Catalog Generator

Prosty skrypt generujący katalog produktów na podstawie pliku CSV (TSV) i szablonu w formacie HTML — wynik w formacie HTML i PDF.

## Wymagania
- Python 3.8+
- Zewnętrzny program: [wkhtmltopdf](https://wkhtmltopdf.org/)

## Instalacja

```bash
pip install -r requirements.txt
cp .env.example .env
```


W pliku .env ustaw ścieżkę do wkhtmltopdf


## Użycie

Uruchom skrypt:
```bash
python generate_catalog.py
```

Wynik:
W folderze output/ znajdziesz pliki catalog.html i catalog.pdf
