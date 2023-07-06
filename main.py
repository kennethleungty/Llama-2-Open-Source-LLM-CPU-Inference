import box
import timeit
import yaml
import uvicorn
from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.functions import setup_dbqa

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=['GET', 'POST', 'OPTIONS'],
    allow_headers=['*'],
    allow_credentials=True
)

# Load environment variables from .env file
load_dotenv(find_dotenv())

# Import config vars
with open('config/config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))



@app.get("/")
async def generate_llm_response(query: str):
    # Load DBQA object
    start = timeit.default_timer()
    dbqa = setup_dbqa()
    end = timeit.default_timer()
    print(f"Time to load DBQA: {end - start}")

start = timeit.default_timer()
query = 'How many days of maternity leave do I have?'
response = dbqa({'query': query})
end = timeit.default_timer()
print(response)
print(f"Time to retrieve response: {end - start}")

    return {"response": response}
