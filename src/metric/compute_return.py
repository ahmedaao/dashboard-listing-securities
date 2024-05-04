"""Module containing functions which compute return"""


def cumulative_return(curent_price: float, original_price: float) -> float:
    """Calculate the cumulative return of a security
    Source: https://www.investopedia.com/terms/c/cumulativereturn.asp

    Args:
        curent_price (float): Current price of the security
        original_price (float): Original price of the security

    Returns:
        float: Cumulative return as a ratio for the security
    """
    result = (curent_price - original_price) / original_price

    return result


def annualized_return(days_held: float, cum_return: float) -> float:
    """Calculate the annualized return for a security

    Args:
        days_held (float): Number of days the security was held
        cum_return (float): Cumulative return during the number of days
    """
    result = ((1 + cum_return) ** (365 / days_held)) - 1

    return result


def required_annualized_return(
    current_price: float, required_price: float, nb_years: int
):
    """Calculate the required annualized return to reach required price
    in x years

    Args:
        current_price (float): Current price of the security
        required_price (float): Price to reach
        nb_years (int): Number of years to reach required price

    Returns:
        float: Required annualized return to reach required price
    """
    result = ((required_price / current_price) ** (1 / nb_years)) - 1

    return result
