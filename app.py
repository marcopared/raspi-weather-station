from multiprocessing import Process, Manager
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles   # Used for serving static files
from fastapi.templating import Jinja2Templates
import uvicorn
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
import requests
import os
import init_db

# Data visualization using Plotly Express
import plotly.express as px

from urllib.request import urlopen
import json
import time

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

PORT_NUMBER = 6543
API_URL = f"raspberrypi.local:{PORT_NUMBER}"

start_time = time.time()

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/data", response_class=JSONResponse)
async def get_data():
    return {
        "time_data": list(time_data),
        "light_data": list(light_data),
        "humidity_data": list(humidity_data),
        "temp_data": list(temp_data)
    }

@app.post("/api/store-data")
def store_data(data: dict):
    load_dotenv("credentials.env")
    init_db.add_to_db(
        user=os.environ['MYSQL_USER'],
        password=os.environ['MYSQL_PASSWORD'],
        host=os.environ['MYSQL_HOST'],
        db_name=os.environ['MYSQL_DATABASE'],
        table_name='Weather',
        light=data['light'],
        humidity=data['humidity'],
        temp=data['temp']
    )

def gen_sample_data(light_data, humidity_data, temp_data, time_data):
    # Data represented in dictionaries
    print("Generating now")
    for i in range(50):
        light_data.append(i)
        humidity_data.append(i*0.1)
        temp_data.append(i*10)

        time_data.append(int(time.time() - start_time))
        # print("Generated data")
        # print("Light:", light_data)
        # print("Humidity:", humidity_data)
        # print("Temperature:", temp_data)
# print("Time:", time_data)~
        time.sleep(1)

def collect_data(light_data, humidity_data, temp_data, time_data):
    """
    Every several seconds, make requests to the Raspberry Pi API to collect sensor data and store it in the SQL database, then make a request to Raspberry Pi API to display the most recent weather data on the LCD.
    """
    for _ in range(50): 
        light_response = requests.get(f"http://{API_URL}/light-reading")
        dht_response = requests.get(f"http://{API_URL}/dht-reading")

        light_val = json.loads(light_response.content)['value']
        light_data.append(light_val)
        dht_data = json.loads(dht_response.content)
        humidity_data.append(dht_data['humidity'])
        temp_data.append(dht_data['temp'])
        time_data.append(int(time.time() - start_time))

        print("light_data:", light_data)
        print("dht_data:", dht_data)

        data = {"light": light_val, "humidity": dht_data['humidity'], "temp": dht_data['temp']}
        data = json.dumps(data)

        requests.post(f"http://{API_URL}/set-lcd", data)
        requests.post("http://localhost:8000/api/store-data", data)
        # db_manager.add(light_val, dht_data['humidity'], dht_data['temp'])
        
        
if __name__ == "__main__":
    manager = Manager()

    light_data = manager.list()
    humidity_data = manager.list()
    temp_data = manager.list()
    time_data = manager.list()

    debug = False
    if debug:
        p = Process(target=gen_sample_data, args=(light_data, humidity_data, temp_data, time_data))
    else:
        p = Process(target=collect_data, args=(light_data, humidity_data, temp_data, time_data))


    try:
        p.start()
        print("Running server.")
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except KeyboardInterrupt:
        print("Application closed.")
    finally:
        # print("Adding values to database.")
        # db_manager.add_all(list(light_data), list(humidity_data), list(temp_data))
        p.join()
        # db_manager.exit()


