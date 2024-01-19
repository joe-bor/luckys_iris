from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import asyncio
import os
import shutil
import logging
from .utils.barcode_utils import process_pdf

# Instantiate app
app = FastAPI()


app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')


@app.get('/', response_class=HTMLResponse)
async def upload_form(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.post('/upload')
async def handle_file_upload(file: UploadFile = File(...)):
    temp_file = f'temp_{file.filename}'
    barcode_dir = 'static/barcodes'
    os.makedirs(barcode_dir, exist_ok=True)
    
    # save the uploaded file locally
    try:
        with open(temp_file, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
        # generate barcodes - svgs
        product_descriptions, barcode_counter = process_pdf(temp_file, barcode_dir)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # delete the uploaded file
        if os.path.exists(temp_file):
            os.remove(temp_file)
    
  # Generate HTML content with responsive two-column layout
    html_content = """
    <html>
    <head>
    <style>
        h3 {
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .container {
            column-count: 2;
            column-gap: 20px;
        }
        .barcode-item {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
            break-inside: avoid;
        }
        .barcode-item img {
            max-width: 100%;
            height: auto;
        }
        .description {
            margin-left: 10px;
        }
        @media screen and (max-width: 768px) {
            .container {
                column-count: 1;
            }
        }
    </style>
    </head>
    <body>
    """
    html_content += f'''
    <h3>Number of barcodes generated: {barcode_counter} | NOTE: There's 30 rows in a full page.</h3>
    <div class="container">
    '''

    for product_number, description in product_descriptions.items():
        barcode_file = f"/{barcode_dir}/{product_number}.svg"
        html_content += f'<div class="barcode-item"><img src="{barcode_file}" alt="Barcode"><span class="description">{description}</span></div>'
    html_content += "</div></body></html>"

    clean_up_delay = int(os.getenv("DELAY", 20))
    asyncio.create_task(delete_all_svg(barcode_dir, clean_up_delay))
    
    # Return the HTML response
    return HTMLResponse(content=html_content)

@app.get('/cleanup')
async def cleanup_svgs():
    barcode_dir = 'static/barcodes'
    await delete_all_svg(barcode_dir)
    return {"message": f"All barcodes in {barcode_dir} have been deleted."}


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

# uvicorn app.main:app --reload