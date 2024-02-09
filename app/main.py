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
async def handle_file_upload(request: Request, file: UploadFile = File(...)):
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

    clean_up_delay = int(os.getenv("DELAY", 20))
    asyncio.create_task(delete_all_svg(barcode_dir, clean_up_delay))
    
    # Return the HTML response
    return templates.TemplateResponse('barcodes.html', {
        'request': request,
        'barcode_counter': barcode_counter,
        'product_descriptions': product_descriptions
    })

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