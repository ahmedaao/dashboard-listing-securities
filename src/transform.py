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

    output_dict = input_dict
    output_dict['last_date'] = last_dates
    output_dict['last_price'] = last_prices
    return output_dict


def group_by(attributes: list, input_dict: dict) -> dict:
    """
    Groups data by specified columns and aggregate others.

    Args:
        input_dict (dict): A dictionary of all transactions.
        attributes (list): List of column names to group by.

    Returns:
        dict: A dictionary with grouped data.
    """
    # Convert the dictionary to a pandas DataFrame
    df = pd.DataFrame(input_dict)

    # Group by the specified columns and aggregate
    grouped_df = df.groupby(attributes).agg({
        'quantity': 'sum',
        'total_price': 'sum'
    }).reset_index()

    grouped_df['cost_price'] = grouped_df['total_price'] / grouped_df['quantity']

    # Reorder columns to ensure 'total_price' is last
    columns_order = [col for col in grouped_df.columns if col != 'total_price'] + ['total_price']
    grouped_df = grouped_df[columns_order]

    output_dict = grouped_df.to_dict('list')
    return output_dict


def merge_dictionary(input_dict_1: dict, input_dict_2: dict) -> dict:
    """
    Merges two dictionaries on the 'isin' column.

    Parameters:
    input_dict_1 (dict): The first dictionary.
    input_dict_2 (dict): The second dictionary.

    Returns:
        output_dict: The merged dictionary.
    """
    # Convert dictionaries to pandas DataFrames
    df1 = pd.DataFrame(input_dict_1)
    df2 = pd.DataFrame(input_dict_2)

    # Merge the two dataframes on the 'isin' column
    merged_df = pd.merge(df1, df2, on='isin', how='inner')
    output_dict = merged_df.to_dict('list')
    return output_dict


def add_cumulative_return(input_dict: dict) -> dict:
    """
    Calculate the cumulative return for a set of transactions.

    This function takes a dictionary with transaction data, converts it to a pandas DataFrame,
    computes the total last price and the cumulative return for each transaction, and returns the updated
    data as a dictionary with lists.

    Parameters:
    input_dict (dict): A dictionary containing transaction data

    Returns:
    dict: input_dict + these new keys (total_last_price, cumulative_return)
    """
    df = pd.DataFrame(input_dict)
    df['total_last_price'] = df['quantity'] * df['last_price']
    df['cumulative_return'] = (df['total_last_price'] - df['total_price']) / df['total_price']

    output_dict = df.to_dict('list')
    return output_dict
