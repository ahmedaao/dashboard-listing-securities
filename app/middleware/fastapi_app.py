import os
import requests
import pandas as pd
import yfinance as yf
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from config import ROOT_DIR
import src.extract
import src.extract.extract
import src.transforms.aggregate
import src.transforms.add_attribute


class inputData(BaseModel):
    attribute: str


templates = Jinja2Templates(directory="templates")
db_file = os.path.join(ROOT_DIR, "app", "backend", "database.db")


app = FastAPI(title="MyApp", description="Real Time Stock Price Tracker")


@app.get("/")
def read_root():
    """Welcome message to test the API"""
    return {"message": "Welcome to the Real Time Stock Price Tracker"}


@app.post("/overview")
async def overview(request: inputData):
    attribute = request.attribute

    dict_attribute = src.extract.extract.by_attribute(db_file, attribute)
    df_attribute = pd.DataFrame(dict_attribute)
    groupby_attribute = src.transforms.aggregate.sum_by_attribute(
        attribute[:-2], df_attribute
    )
    result = src.transforms.add_attribute.last_price(
        attribute[:-2], groupby_attribute
    )

    return result


# @app.post("/get_stock_data")
# async def get_stock_data(isin: str):
#     data = yf.Ticker(isin).history(period="1y")
#     return {"currentPrice": data["Close"].iloc[-1], "openPrice": data["Open"].iloc[-1]}
