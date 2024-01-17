import tabula
import barcode
from barcode.writer import SVGWriter
import os
import logging

def generate_barcode(upc_code, filename):
    UPC = barcode.get_barcode_class('upc')
    upc = UPC(upc_code, writer=SVGWriter())
    upc.save(filename)

def process_pdf(file_path, barcode_dir):
    product_descriptions = {}
    dfs = tabula.read_pdf(file_path, pages="all")
    barcode_counter = 0

    for i, df in enumerate(dfs):
        try:
            df.columns = [col.strip() for col in df.columns]

            # Initialize empty columns for 'Code' and 'UPC'
            df['Code'] = None
            df['UPC'] = None

            # Handle different column format on page 24
            if 'Code UPC' in df.columns:
                for index, row in df.iterrows():
                    code_upc = row['Code UPC']
                    if ' ' in code_upc:
                        # Standard format with space
                        df.at[index, 'Code'], df.at[index, 'UPC'] = code_upc.split(' ', 1)
                    else:
                        # Non-standard format
                        logging.warning(f"Non-standard format found in 'Code UPC': {code_upc}")

                # Drop unnecessary columns
                df = df.drop(columns=['Code UPC', 'Unnamed: 0', 'Unnamed: 1'])

            # Process the required columns
            df = df[['Product', 'Order', 'Description', 'Code', 'UPC']].dropna(subset=['UPC'])
            for index, row in df.iterrows():
                upc_number = str(row['UPC']).zfill(12)
                description = row['Description']
                barcode_file = os.path.join(barcode_dir, upc_number)
                generate_barcode(upc_number, barcode_file)
                product_descriptions[upc_number] = description
                barcode_counter += 1

        except Exception as e:
            logging.error(f'Error processing page {i + 1}: {e}')

    logging.info(f'Total number of barcodes generated: {barcode_counter}')
    return product_descriptions
