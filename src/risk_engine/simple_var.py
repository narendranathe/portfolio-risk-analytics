"""
Value at Risk (VaR) Calculator
Demonstrates financial risk analytics for hedge funds
"""

import numpy as np
from typing import List


class SimpleVaRCalculator:
    """Calculate Value at Risk for a portfolio"""
    
    def __init__(self, confidence_level: float = 0.95):
        self.confidence_level = confidence_level
        self.alpha = 1 - confidence_level
    
    def calculate_var(self, returns: List[float], portfolio_value: float) -> dict:
        """
        Calculate Value at Risk
        
        Parameters:
        - returns: List of historical daily returns (as decimals, e.g., 0.01 for 1%)
        - portfolio_value: Total portfolio value in dollars
        
        Returns:
        - Dictionary with VaR results
        """
        returns = np.array(returns)
        sorted_returns = np.sort(returns)
        
        var_index = int(len(sorted_returns) * self.alpha)
        var_return = sorted_returns[var_index]
        var_amount = abs(var_return * portfolio_value)
        
        cvar_returns = sorted_returns[:var_index]
        cvar_return = np.mean(cvar_returns)
        cvar_amount = abs(cvar_return * portfolio_value)
        
        return {
            'confidence_level': self.confidence_level,
            'portfolio_value': portfolio_value,
            'var_amount': round(var_amount, 2),
            'var_percentage': round((var_amount / portfolio_value) * 100, 2),
            'cvar_amount': round(cvar_amount, 2),
            'worst_return': round(sorted_returns[0] * 100, 2),
            'best_return': round(sorted_returns[-1] * 100, 2)
        }


def demo():
    """Demonstrate VaR calculation"""
    print("=" * 80)
    print("VALUE AT RISK (VaR) CALCULATOR DEMO")
    print("=" * 80)
    print()
    
    np.random.seed(42)
    returns = np.random.normal(0.0005, 0.015, 252)
    portfolio_value = 10_000_000
    
    calculator = SimpleVaRCalculator(confidence_level=0.95)
    results = calculator.calculate_var(returns.tolist(), portfolio_value)
    
    print(f"Portfolio Value: ${results['portfolio_value']:,}")
    print(f"Confidence Level: {results['confidence_level']*100}%")
    print()
    print(f"📉 95% VaR: ${results['var_amount']:,}")
    print(f"   This means: In 95% of cases, daily loss will not exceed ${results['var_amount']:,}")
    print(f"   ({results['var_percentage']}% of portfolio)")
    print()
    print(f"📉 95% CVaR (Expected Shortfall): ${results['cvar_amount']:,}")
    print(f"   This means: If we exceed VaR, average loss is ${results['cvar_amount']:,}")
    print()
    print(f"Best Daily Return: +{results['best_return']}%")
    print(f"Worst Daily Return: {results['worst_return']}%")
    print()
    print("=" * 80)


if __name__ == "__main__":
    demo()
