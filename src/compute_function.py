"""Module containing functions for basic operation"""

from typing import List
import pandas as pd


def rolling_variation(lst: List[float], window_size: int) -> List:
    """
    Calculate rolling variations in a list.

    Args:
    lst (List[float]): The input list of numerical elements.
    window_size (int): The size of the rolling window.

    Returns:
    List[float]: A list containing the rolling variations.
    """
    series = pd.Series(lst)
    rolling_variations = series.rolling(window=window_size).apply(lambda x: (x[-1] - x[0]) / x[0], raw=True)
    return rolling_variations.tolist()[window_size - 1:]
