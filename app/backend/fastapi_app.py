import requests
import yfinance as yf
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


class TickerData(BaseModel):
    isin: str


app = FastAPI(title="MyApp", description="Real Time Stock Price Tracker")


templates = Jinja2Templates(directory="templates")

# @app.get("/")
# def read_root():
# return {"Hello": "World"}


@app.get("/hello-world", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "name": "World"}
    )


@app.post("/get_stock_data")
async def get_stock_data(isin: str):
    data = yf.Ticker(isin).history(period="1y")
    return {"currentPrice": data["Close"].iloc[-1], "openPrice": data["Open"].iloc[-1]}


if __name__ == "__main__":
    app.run(debug=True)
