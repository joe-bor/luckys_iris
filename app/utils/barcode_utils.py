import tabula
import barcode
from barcode.writer import SVGWriter
import os

def generate_barcode(upc_code, filename):
    UPC = barcode.get_barcode_class('upc')
    upc = UPC(upc_code, writer=SVGWriter())
    upc.save(filename)

def process_pdf(file_path, barcode_dir):
    product_descriptions = {}
    dfs = tabula.read_pdf(file_path, pages='all')

    for df in dfs:
        df = df[['Product', 'Order', 'Description', 'Code', 'UPC']]
        for index, row in df.iterrows():
            upc_number = str(row['UPC']).zfill(12)
            description = row['Description']
            barcode_file = os.path.join(barcode_dir, f"{upc_number}.svg")
            generate_barcode(upc_number, barcode_file)
            product_descriptions[upc_number] = description
    
    return product_descriptions
