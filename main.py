import tabula
import barcode
from barcode.writer import SVGWriter
import os

# Read pdf into list of DataFrame
dfs = tabula.read_pdf("iris.pdf", pages='all')

print(type(dfs))
print(len(dfs))

# -------------------------------------------------

# Create a directory to save barcodes
os.makedirs('barcodes', exist_ok=True)

def generate_barcode(upc_code, filename):
    UPC = barcode.get_barcode_class('upc')
    upc = UPC(upc_code, writer=SVGWriter())
    upc.save(filename)

for df in dfs:
    # Selecting only required columns (up to UPC)
    df = df[['Product', 'Order', 'Description', 'Code', 'UPC']]

    # Generating barcodes for each product
    for index, row in df.iterrows():
        product_number = str(row['Product'])
        # Ensure product number is 12 digits for UPC-A
        product_number = product_number.zfill(12)
        
        barcode_file = f"barcodes/{product_number}"
        generate_barcode(product_number, barcode_file)



html_content = "<html><body>"

# Directory containing the barcode SVG files
barcode_dir = 'barcodes'

# Loop through each file in the directory
for filename in os.listdir(barcode_dir):
    if filename.endswith(".svg"):
        # Construct the path to the barcode file
        filepath = os.path.join(barcode_dir, filename)
        
        # Add an img tag for the barcode
        html_content += f'<img src="{filepath}" alt="{filename}"><br>'

html_content += "</body></html>"

# Write the HTML content to a file
with open("barcodes.html", "w") as html_file:
    html_file.write(html_content)
