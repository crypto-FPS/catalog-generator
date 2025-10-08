import os
import pandas as pd
from jinja2 import Environment, FileSystemLoader
from collections import defaultdict
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
from weasyprint import HTML
from PIL import Image
import requests
from io import BytesIO as IOBytes


CSV_PATH = 'data/products.csv'
TEMPLATE_DIR = 'templates'
TEMPLATE_FILE = 'catalog_template.html'
OUTPUT_HTML = 'output/catalog.html'
OUTPUT_PDF = 'output/catalog.pdf'
TEMP_IMG_DIR = 'temp_images'

os.makedirs('output', exist_ok=True)
os.makedirs(TEMP_IMG_DIR, exist_ok=True)


def parse_product(row):
    return {
        'name': str(row['name']).strip(),
        'category': str(row['category']).strip(),
        'image': str(row['images 1']).strip()
    }


def group_products(df):
    grouped = defaultdict(list)
    for _, row in df.iterrows():
        product = parse_product(row)
        grouped[product['category']].append(product)
    return dict(grouped)


def download_and_resize_image(url, max_height=250):
    try:
        response = requests.get(url)
        response.raise_for_status()
        img = Image.open(IOBytes(response.content)).convert("RGB")

        h_percent = max_height / img.height
        new_width = int(img.width * h_percent)
        img = img.resize((new_width, max_height), Image.LANCZOS)

        filename = os.path.basename(url).split('?')[0]
        local_path = os.path.join(TEMP_IMG_DIR, filename)
        img.save(local_path, format='JPEG', quality=85)
        return local_path
    except Exception as e:
        print(f"Nie udało się pobrać lub przetworzyć obrazka: {url} -> {e}")
        return url


def clean_temp_images():
    for filename in os.listdir(TEMP_IMG_DIR):
        file_path = os.path.join(TEMP_IMG_DIR, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Nie udało się usunąć pliku {file_path}: {e}")


def merge():
    merger = PdfWriter()
    for pdf in ["assets/okladka.pdf", OUTPUT_PDF, "assets/strona_kontaktowa.pdf"]:
        merger.append(pdf)
    merger.write("output/catalog.pdf")
    merger.close()
    print("Połączono pliki w output/result.pdf")


def numerate():
    pdfmetrics.registerFont(TTFont("ImFellEnglishSC", "assets/ImFellEnglishSC.ttf"))

    reader = PdfReader(OUTPUT_PDF)
    writer = PdfWriter()

    for i, page in enumerate(reader.pages, start=1):
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=A4)
        can.setFont("ImFellEnglishSC", 16)
        can.drawString(550, 28, str(i))
        can.save()
        packet.seek(0)

        num_pdf = PdfReader(packet)
        num_page = num_pdf.pages[0]
        page.merge_page(num_page)
        writer.add_page(page)

    with open(OUTPUT_PDF, "wb") as f:
        writer.write(f)

    merge()


def generate_catalog():
    df = pd.read_csv(CSV_PATH, sep=',')
    grouped_products = group_products(df)

    for category, products in grouped_products.items():
        for p in products:
            p['image'] = download_and_resize_image(p['image'], max_height=200)

    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template(TEMPLATE_FILE)
    html_content = template.render(grouped_products=grouped_products, page_offset=1)

    with open(OUTPUT_HTML, 'w', encoding='utf-8') as file:
        file.write(html_content)

    print(f'HTML zapisano do: {OUTPUT_HTML}')

    HTML(string=html_content, base_url='.').write_pdf(OUTPUT_PDF)
    print(f'PDF zapisano do: {OUTPUT_PDF}')

    numerate()
    clean_temp_images()


if __name__ == '__main__':
    generate_catalog()
