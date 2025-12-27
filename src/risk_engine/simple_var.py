"""
Simple VaR Calculator
Calculates Value at Risk using historical simulation method
"""

import numpy as np
from typing import Tuple


def calculate_var(
    prices: np.ndarray, 
    confidence_95: float = 0.95,
    confidence_99: float = 0.99
) -> Tuple[float, float]:
    """
    Calculate Value at Risk (VaR) using historical simulation method
    
    Args:
        prices: Array of historical prices
        confidence_95: Confidence level for 95% VaR (default: 0.95)
        confidence_99: Confidence level for 99% VaR (default: 0.99)
    
    Returns:
        Tuple of (VaR at 95% confidence, VaR at 99% confidence)
    
    Example:
        >>> prices = np.array([100, 102, 98, 101, 99])
        >>> var_95, var_99 = calculate_var(prices)
        >>> print(f"VaR 95%: ${var_95:.2f}, VaR 99%: ${var_99:.2f}")
    """
    
    if len(prices) < 2:
        raise ValueError("Need at least 2 price observations")
    
    # Convert to numpy array if not already
    prices = np.array(prices)
    
    # Calculate returns
    returns = np.diff(prices) / prices[:-1]
    
    # Calculate VaR at different confidence levels
    var_95 = np.percentile(returns, (1 - confidence_95) * 100)
    var_99 = np.percentile(returns, (1 - confidence_99) * 100)
    
    # Convert to dollar values based on current price
    current_price = prices[-1]
    var_95_dollar = abs(var_95 * current_price)
    var_99_dollar = abs(var_99 * current_price)
    
    return var_95_dollar, var_99_dollar


def calculate_var_from_returns(
    returns: np.ndarray,
    current_value: float,
    confidence_level: float = 0.95
) -> float:
    """
    Calculate VaR from returns array
    
    Args:
        returns: Array of historical returns
        current_value: Current portfolio value
        confidence_level: Confidence level (default: 0.95)
    
    Returns:
        VaR in dollar terms
    """
    
    if len(returns) < 2:
        raise ValueError("Need at least 2 return observations")
    
    # Calculate VaR
    var_percentile = np.percentile(returns, (1 - confidence_level) * 100)
    var_dollar = abs(var_percentile * current_value)
    
    return var_dollar


def calculate_portfolio_var(
    portfolio_values: np.ndarray,
    confidence_level: float = 0.95
) -> float:
    """
    Calculate VaR for a portfolio
    
    Args:
        portfolio_values: Array of historical portfolio values
        confidence_level: Confidence level (default: 0.95)
    
    Returns:
        Portfolio VaR in dollar terms
    """
    
    if len(portfolio_values) < 2:
        raise ValueError("Need at least 2 portfolio value observations")
    
    # Calculate portfolio returns
    returns = np.diff(portfolio_values) / portfolio_values[:-1]
    
    # Calculate VaR
    current_value = portfolio_values[-1]
    var_dollar = calculate_var_from_returns(returns, current_value, confidence_level)
    
    return var_dollar


if __name__ == "__main__":
    # Test the VaR calculator
    print("=" * 80)
    print("VaR CALCULATOR TEST")
    print("=" * 80)
    print()
    
    # Sample price data
    prices = np.array([100, 102, 98, 101, 99, 103, 97, 100, 102, 98])
    
    print(f"Sample prices: {prices}")
    print(f"Number of observations: {len(prices)}")
    print()
    
    # Calculate VaR
    var_95, var_99 = calculate_var(prices)
    
    print(f"Current Price: ${prices[-1]:.2f}")
    print(f"VaR (95% confidence): ${var_95:.2f}")
    print(f"VaR (99% confidence): ${var_99:.2f}")
    print()
    
    print("Interpretation:")
    print(f"  - There is a 95% chance that losses will not exceed ${var_95:.2f}")
    print(f"  - There is a 99% chance that losses will not exceed ${var_99:.2f}")
    print()
    print("=" * 80)