from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from search import get_result
import os
import logging

PUBLIC_DIRECTORY = "./client/build"

app = FastAPI()

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


@app.get("/s/{query}")
async def search(query):
    result, time = get_result(query)
    return result, time

@app.get("/")
async def root():
    return FileResponse(f"{PUBLIC_DIRECTORY}/index.html")

@app.get("/{file}.{ext}")
async def file(file:str, ext: str):
    file_path = f"{PUBLIC_DIRECTORY}/{file}.{ext}"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        return RedirectResponse("/")

@app.get("/{path}")
async def path():
    return FileResponse(f"{PUBLIC_DIRECTORY}/index.html")

@app.get("/{path}/{name}")
async def path_name():
    return FileResponse(f"{PUBLIC_DIRECTORY}/index.html")

app.mount("/", StaticFiles(directory=PUBLIC_DIRECTORY), name="public")

