import os
import pdfkit
import pandas as pd
from jinja2 import Environment, FileSystemLoader
from collections import defaultdict
from dotenv import load_dotenv

load_dotenv()

CSV_PATH = 'data/products.csv'
TEMPLATE_DIR = 'templates'
TEMPLATE_FILE = 'catalog_template.html'
OUTPUT_HTML = 'output/catalog.html'
OUTPUT_PDF = 'output/catalog.pdf'
WKHTMLTOPDF_PATH = os.getenv('WKHTMLTOPDF_PATH')


os.makedirs('output', exist_ok=True)


def parse_product(row):
    parts = [part.strip() for part in row['name'].split('/')]
    main_name = parts[0] if len(parts) > 0 else row['name']
    category = parts[1] if len(parts) > 1 else 'Brak kategorii'
    variant = parts[2] if len(parts) > 2 else ''
    return {
        'main_name': main_name,
        'variant': variant,
        'category': category,
        'image': row['image']
    }

def group_products(df):
    grouped = defaultdict(list)
    for _, row in df.iterrows():
        product = parse_product(row)
        grouped[product['category']].append(product)
    return dict(grouped)

def generate_catalog():
    df = pd.read_csv(CSV_PATH, sep='\t')


    grouped_products = group_products(df)


    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template(TEMPLATE_FILE)


    html_content = template.render(grouped_products=grouped_products)

    with open(OUTPUT_HTML, 'w', encoding='utf-8') as file:
        file.write(html_content)

    print(f'HTML catalog generated at: {OUTPUT_HTML}')


    config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)
    options = {
        'page-size': 'A4',
        'margin-top': '0cm',
        'margin-right': '0cm',
        'margin-bottom': '0cm',
        'margin-left': '0cm',
        'encoding': "UTF-8"
    }
    pdfkit.from_file(OUTPUT_HTML, OUTPUT_PDF, configuration=config, options=options)

    print(f'PDF catalog generated at: {OUTPUT_PDF}')

if __name__ == '__main__':
    generate_catalog()
