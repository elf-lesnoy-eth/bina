import os
import pandas as pd
import folium

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    df = pd.read_csv("static/apartments.csv")
    map_center = [df.latitude.mean(), df.longitude.mean()]
    m = folium.Map(location=map_center, zoom_start=12)

    for _, row in df.iterrows():
        folium.Marker(
            location=[row.latitude, row.longitude],
            popup=row.address,
            icon=folium.Icon(color="blue", icon="home")
        ).add_to(m)

    m.save("templates/map.html")
    return templates.TemplateResponse("map.html", {"request": request})