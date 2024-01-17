import uvicorn
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    load_dotenv()
    
    port = int(os.getenv('PORT', 8000))
    
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)