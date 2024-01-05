from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

# Instantiate app
app = FastAPI()

# Directory for barcode svgs
os.makedirs('static/barcodes', exist_ok=True)

app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')


@app.get('/', response_class=HTMLResponse)
async def upload_form(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.post('/upload')
async def handle_file_upload(file: UploadFile = File(...)):
    # process the file, generate barcodes
    # import from previous main_2
    
    # redirect to results page that contains the generated html
    pass
    return HTMLResponse()