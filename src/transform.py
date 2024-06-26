"""This module contains functions making transformation (add attributes
and feature engineering)
"""

import yfinance as yf


def keep_attributes(input_dict, keys_to_keep):
    """
    Filters a dictionary by retaining only the specified keys.

    :param input_dict: The original dictionary.
    :param keys_to_keep: A list of keys to retain in the new dictionary.
    :return: A new dictionary containing only the specified keys.
    """
    return {key: input_dict[key] for key in keys_to_keep if key in input_dict}
