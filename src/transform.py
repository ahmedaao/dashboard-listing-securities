"""This module contains functions making transformation (add attributes
and feature engineering)
"""

import yfinance as yf
import pandas as pd


def keep_attribute(input_dict: dict, keys_to_keep: list) -> dict:
    """
    Filters a dictionary by retaining only the specified keys.

    :param input_dict: The original dictionary.
    :param keys_to_keep: A list of keys to retain in the new dictionary.
    :return: A new dictionary containing only the specified keys.
    """
    return {key: input_dict[key] for key in keys_to_keep if key in input_dict}


def remove_duplicate(input_dict: dict) -> dict:
    """
    Remove duplicates from the list of values associated with any key in the input dictionary.

    Parameters:
    input_dict (dict): A dictionary where the values are lists of strings.

    Returns:
    dict: The same dictionary with duplicates removed from the list of values.
    """
    # Iterate through each key in the dictionary
    for key in input_dict:
        # Use set to remove duplicates, then convert back to list
        input_dict[key] = list(set(input_dict[key]))

    return input_dict


def add_cost_price(input_dict: dict) -> dict:
    """
    Groups data by 'isin' and calculates the total quantity and average cost price.

    Args:
        input_dict (dict): A dictionnary of all transactions

    Returns:
        dict: A dictionnary with the sum of quantity and the cost price per isin
    """
    # Convert the dictionary to a pandas DataFrame
    df = pd.DataFrame(input_dict)

    # Group by 'isin' and calculate the sum of 'quantity' and the mean of 'transaction_price'
    grouped_df = df.groupby(['isin', 'isin_name']).agg({
        'quantity': 'sum',
        'transaction_price': 'mean'
    }).reset_index()

    # Rename the column 'transaction_price' to 'cost_price' in the grouped DataFrame
    grouped_df.rename(columns={'transaction_price': 'cost_price'}, inplace=True)

    # Convert the DataFrame to a dictionary with the required format
    result = {
        'isin': grouped_df['isin'].tolist(),
        'isin_name': grouped_df['isin_name'].tolist(),
        'quantity': grouped_df['quantity'].tolist(),
        'cost_price': grouped_df['cost_price'].tolist()
    }

    return result


def add_last_price(input_dict: dict):
    """
    Add the latest stock prices to the input dictionary for each ISIN using yfinance.

    Parameters:
    input_dict (dict): A dictionary with ISINs as values in a list.

    Returns:
    dict: The same dictionary with a new key 'last_price' containing the last stock prices.
    """
    # Initialize a dictionary to store the latest dates and values
    last_dates = []
    last_prices = []

    # Iterate through each ISIN in the input dictionary
    for isin in input_dict['isin']:
        # Get the stock symbol from ISIN. This part might need a mapping function if the ISIN doesn't directly map to a symbol.
        stock = yf.Ticker(isin)
        # Retrieve the latest market data
        stock_history = stock.history(period='1mo')['Close']
        last_date = stock_history.index[-1].date()
        last_price = stock_history.iloc[-1]
        # Store the latest dates and prices in the dictionary
        last_dates.append(last_date)
        last_prices.append(last_price)

    input_dict['last_date'] = last_dates
    input_dict['last_price'] = last_prices
    return input_dict
