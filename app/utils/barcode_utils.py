import tabula
import barcode
from barcode.writer import SVGWriter
import os
import logging
import asyncio

def generate_barcode(upc_code, filename):
    UPC = barcode.get_barcode_class('upc')
    upc = UPC(upc_code, writer=SVGWriter())
    upc.save(filename)

def process_pdf(file_path, barcode_dir):
    product_descriptions = {}
    barcode_counter = 0
    dfs = tabula.read_pdf(file_path, pages="all")

    # Iterate through list of DataFrames
    for i, df in enumerate(dfs):
        # sanitize column names
        df.columns = [col.strip() for col in df.columns]

        # --Unexpected Errors--
        if 'Code UPC' in df.columns:
            df['Code'], df['UPC'] = zip(*df['Code UPC'].apply(lambda x: x.split(' ', 1) if ' ' in x else (None, None)))
            df = df.drop(columns=['Code UPC', 'Unnamed: 0', 'Unnamed: 1'])
        # -- End --

        df = df[['Product', 'Order', 'Description', 'Code', 'UPC']].dropna(subset=['UPC'])
        for index, row in df.iterrows():
            try:
                upc_number = str(row['UPC']).zfill(12)
                description = row['Description']
                order_qty = row['Order']
                product_descriptions[upc_number] = (description, order_qty)
                
                barcode_file = os.path.join(barcode_dir, upc_number)
                generate_barcode(upc_number, barcode_file)
                barcode_counter += 1
            except Exception as e:
                logging.error(f'Error generating barcode on page {i + 1}, row {index}: {e}')

    print(f'Total number of barcodes generated: {barcode_counter}')
    return product_descriptions, barcode_counter

# Helper function for cleaning up barcodes
async def delete_all_svg(barcode_dir, delay=0):
    logging.info(f"Starting cleanup of SVGs with delay {delay} seconds")
    
    await asyncio.sleep(delay=delay)
    
    for file in os.listdir(barcode_dir):
        file_path = os.path.join(barcode_dir, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
            
    logging.info(f"All images in {barcode_dir} have been deleted")
    return {"message": f'All images in {barcode_dir} have been deleted'}