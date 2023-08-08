from fastapi import FastAPI, Request, Form
from fastapi.responses import Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles   # Used for serving static files
import uvicorn
from fastapi.responses import RedirectResponse
import os

from time import sleep, strftime
from urllib.request import urlopen
import json

from reader import Reader

app = FastAPI()
reader = Reader()
app.mount("/static", StaticFiles(directory="static"), name="static")
   
@app.get("/light-reading", response_class=JSONResponse)
def get_light_reading():
    return reader.read_light()

@app.get("/dht-reading", response_class=JSONResponse)
def get_dht_reading():
    return reader.read_dht()

@app.post("/set-lcd")
def set_lcd(data: dict):
    reader.set_lcd(data["light"], data["humidity"], data["temp"])



if __name__ == "__main__":
    debug = False
    if debug:
        try:
            reader.debug_loop()
        except KeyboardInterrupt:
            reader.destroy_all()
    else:
        uvicorn.run(app, host="0.0.0.0", port=6543)
