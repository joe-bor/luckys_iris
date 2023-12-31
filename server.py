import uvicorn
import os
from dotenv import load_dotenv

if __name__ == "__name__":
    load_dotenv()
    
    port = int(os.getenv('PORT', 8000))
    
    uvicorn.run("main:app", host="0.0.0.0", port=port)