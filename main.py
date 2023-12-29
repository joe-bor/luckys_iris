import tabula
import barcode
from barcode.writer import SVGWriter
import os

# Read pdf into list of DataFrame
dfs = tabula.read_pdf("iris.pdf", pages='all')

print(type(dfs))
print(len(dfs))

# ------------GENERATE BARCODES -------------------------------

# Create a directory to save barcodes
os.makedirs('barcodes', exist_ok=True)

def generate_barcode(upc_code, filename):
    UPC = barcode.get_barcode_class('upc')
    upc = UPC(upc_code, writer=SVGWriter())
    upc.save(filename)

# Dictionary to store product number and its description
product_descriptions = {}

for df in dfs:
    # Selecting only required columns (up to UPC)
    df = df[['Product', 'Order', 'Description', 'Code', 'UPC']]

    # Generating barcodes for each product and storing descriptions
    for index, row in df.iterrows():
        product_number = str(row['Product'])
        description = row['Description']

        # Ensure product number is 12 digits for UPC-A
        product_number = product_number.zfill(12)
        
        barcode_file = f"barcodes/{product_number}"
        generate_barcode(product_number, barcode_file)

        # Store the description in the dictionary
        product_descriptions[product_number] = description

# ----------- GENERATE HTML ----------

html_content = "<html><body>"

# Directory containing the barcode SVG files
barcode_dir = 'barcodes'

# Loop through each file in the directory
for filename in os.listdir(barcode_dir):
    if filename.endswith(".svg"):
        # Extract the product number from the filename
        product_number = filename.split('.')[0]
        
        # Get the description from the dictionary
        description = product_descriptions.get(product_number, "No description")

        # Construct the path to the barcode file
        filepath = os.path.join(barcode_dir, filename)
        
        # Add an img tag for the barcode and the description next to it
        html_content += f'<img src="{filepath}" alt="{filename}"> {description}<br>'

html_content += "</body></html>"

# Write the HTML content to a file
with open("barcodes.html", "w") as html_file:
    html_file.write(html_content)

