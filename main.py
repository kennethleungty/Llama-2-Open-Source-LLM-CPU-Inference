import shutil
import os
from fastapi import FastAPI, Request, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from dbmanager import DatabaseManager
from src.utils import setup_dbqa
import yaml
import box
from dotenv import find_dotenv, load_dotenv
import uvicorn
import argparse
from db_build import run_db_build
from werkzeug.utils import secure_filename
# Load environment variables from .env file
load_dotenv(find_dotenv())

# Import config vars
with open('config/config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))

# Initialize FastAPI app
app = FastAPI()

origins = [
    "http://localhost:3000",  # Allows CORS from your React app in development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/create-directory")
async def create_directory(directory: Request):
    # Replace with your logic to create a directory
    data = await directory.json()
    query_text = data.get('input', 'data')
    try:
        success = os.mkdir(f"data/{query_text}")
        return {"status": "success"}
    except Exception as e:
        return {"status": "fail"}

@app.post("/query")
async def query_model(request: Request):
    data = await request.json()
    query_text = data.get('input', 'What is a windows process?')
    query_directory = data.get('currdir','db_faiss')
    db_mng = DatabaseManager()
    db_conn = db_mng.connect(path=query_directory)
    print(query_text)
    print(query_directory)
    response = db_conn({'query': query_text})

    return response


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile, directory: str =Form(...)):
    
    # Ensure the file is a PDF
    if file.filename.endswith(".pdf"):
        # Sanitize directory and filename
        safe_directory = os.path.join('data', secure_filename(directory))
        safe_filename = secure_filename(file.filename)
        # Ensure the directory exists
        os.makedirs(safe_directory, exist_ok=True)
        # Construct the full path
        full_path = os.path.join(safe_directory, safe_filename)
        with open(full_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
            run_db_build(path=directory, vec_path=directory)
        return {"filename": safe_filename, "directory": safe_directory, "status": "file uploaded"}
    raise HTTPException(status_code=400, detail="File not a PDF")


@app.get("/directories")
async def get_directories():
    directories = os.listdir("data")
    return {"directories": directories}

@app.post("/fetch-files")
async def get_files(directory: Request):

    data = await directory.json()
    
    direc = data.get('input', 'data')
    print(direc)
    try:
        files = os.listdir(f"data/{direc}")
    except Exception as e:
        return {"files": []}
    return {"files": files}

@app.post("/delete-files")
async def delete_files(directory: str):
    data_dir = f"data/{directory}"
    if data_dir.is_dir():
        shutil.rmtree(data_dir)
        data_dir.mkdir()  # Recreate the data directory after deletion
        return {"status": "All files deleted"}
    raise HTTPException(status_code=400, detail="Data directory not found")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the application with different settings.")
    
    # Set up mutually exclusive group for local/online mode
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument("--local", action="store_true", help="Run in local mode")
    mode_group.add_argument("--online", action="store_false", help="Run in online mode (default)", default=False)

    args = parser.parse_args()

    mng = DatabaseManager()
    # run_db_build(args.local)

    # Set local_mode based on the command-line arguments
    if args.local:
        mng.set_local_true()
    else:
        mng.set_local_false()

    uvicorn.run(app, host="0.0.0.0", port=8000)
