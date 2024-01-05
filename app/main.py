from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import shutil
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
        product_descriptions = process_pdf(temp_file, barcode_dir)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # delete the uploaded file
        if os.path.exists(temp_file):
            os.remove(temp_file)
    
    # create an html page containing the svgs
    html_content = "<html><body>"
    for product_number, description in product_descriptions.items():
        barcode_file = f"/static/barcodes/{product_number}.svg"
        html_content += f'<img src="{barcode_file}" alt="Barcode"> {description}<br>'
    html_content += "</body></html>"
    
    # redirect to html page containing the svgs
    return HTMLResponse(content=html_content)