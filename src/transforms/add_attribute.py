"""This module contains functions adding attributes"""
import yfinance as yf


def last_price(attribute: str, data: dict) -> dict:
    """
    Fetches the last closing prices for a list of ISINs and adds them to the dictionary.

    Parameters:
    attribute (str): The key in the dictionary that contains the list of ISINs.
    data (dict): The dictionary containing the list of ISINs and other attributes.

    Returns:
    dict: The updated dictionary with the last closing prices added.
    """
    isin_list = data[attribute]
    previous_close_prices = []

    for isin in isin_list:

        # Add previous close price to dictionary
        stock = yf.Ticker(isin)
        previous_close_price = stock.info['previousClose']
        previous_close_prices.append(previous_close_price)
    data['previousClosePrice'] = previous_close_prices

    # Add total close prices to the dictionary
    quantity = data.get('quantity', [])
    previous_close_prices = data.get('previousClosePrice', [])
    total_close_prices = [q * p for q, p in zip(quantity, previous_close_prices)]
    data['totalClosePrice'] = total_close_prices

    return data
