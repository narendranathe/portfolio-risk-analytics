"""
VaR Analysis and Visualization
Demonstrates portfolio risk metrics with charts
"""

import sys
sys.path.append('src')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from risk_engine.simple_var import SimpleVaRCalculator

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette('husl')

print("=" * 80)
print("PORTFOLIO RISK ANALYTICS - VAR VISUALIZATION")
print("=" * 80)
print()

# Generate sample returns
np.random.seed(42)
returns = np.random.normal(0.0005, 0.015, 252)
portfolio_value = 10_000_000

# Create DataFrame
df_returns = pd.DataFrame({
    'date': pd.date_range(start='2024-01-01', periods=252, freq='B'),
    'daily_return': returns
})

df_returns['cumulative_return'] = (1 + df_returns['daily_return']).cumprod() - 1
df_returns['portfolio_value'] = portfolio_value * (1 + df_returns['cumulative_return'])

# Calculate VaR
var_calc = SimpleVaRCalculator(confidence_level=0.95)
var_results = var_calc.calculate_var(returns.tolist(), portfolio_value)

print('Portfolio Risk Metrics')
print('-' * 80)
print(f"Portfolio Value: ${var_results['portfolio_value']:,}")
print(f"Confidence Level: {var_results['confidence_level']*100}%")
print(f"\n95% VaR: ${var_results['var_amount']:,}")
print(f"VaR Percentage: {var_results['var_percentage']}%")
print(f"\n95% CVaR: ${var_results['cvar_amount']:,}")
print(f"\nBest Return: {var_results['best_return']}%")
print(f"Worst Return: {var_results['worst_return']}%")
print()

# Create visualizations
print("Creating visualizations...")

fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# 1. Portfolio Value Over Time
axes[0, 0].plot(df_returns['date'], df_returns['portfolio_value'], linewidth=2, color='blue')
axes[0, 0].axhline(y=portfolio_value, color='r', linestyle='--', label='Initial Value')
axes[0, 0].set_title('Portfolio Value Over Time', fontsize=14, fontweight='bold')
axes[0, 0].set_xlabel('Date')
axes[0, 0].set_ylabel('Portfolio Value ($)')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# 2. Returns Distribution
axes[0, 1].hist(returns * 100, bins=30, edgecolor='black', alpha=0.7, color='green')
axes[0, 1].axvline(x=np.percentile(returns * 100, 5), color='r', 
                   linestyle='--', linewidth=2, label='5th Percentile (VaR)')
axes[0, 1].set_title('Daily Returns Distribution', fontsize=14, fontweight='bold')
axes[0, 1].set_xlabel('Daily Return (%)')
axes[0, 1].set_ylabel('Frequency')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# 3. Cumulative Returns
axes[1, 0].plot(df_returns['date'], df_returns['cumulative_return'] * 100, linewidth=2, color='purple')
axes[1, 0].fill_between(df_returns['date'], 0, df_returns['cumulative_return'] * 100, alpha=0.3)
axes[1, 0].set_title('Cumulative Returns', fontsize=14, fontweight='bold')
axes[1, 0].set_xlabel('Date')
axes[1, 0].set_ylabel('Cumulative Return (%)')
axes[1, 0].grid(True, alpha=0.3)

# 4. VaR Illustration
sorted_returns = np.sort(returns * 100)
var_threshold = np.percentile(returns * 100, 5)

axes[1, 1].hist(returns * 100, bins=30, edgecolor='black', alpha=0.5, label='All Returns', color='gray')
axes[1, 1].hist(sorted_returns[sorted_returns <= var_threshold], bins=15, 
                color='red', alpha=0.7, label='VaR Exceedances')
axes[1, 1].axvline(x=var_threshold, color='darkred', linestyle='--', 
                   linewidth=2, label=f'VaR Threshold ({var_threshold:.2f}%)')
axes[1, 1].set_title('VaR and Tail Risk', fontsize=14, fontweight='bold')
axes[1, 1].set_xlabel('Daily Return (%)')
axes[1, 1].set_ylabel('Frequency')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()

# Save figure
plt.savefig('docs/var_analysis.png', dpi=300, bbox_inches='tight')
print("✅ Visualization saved to docs/var_analysis.png")

# Show plot
plt.show()

print()
print("=" * 80)
print("ANALYSIS COMPLETE!")
print("=" * 80)
print("\nNext steps:")
print("1. Check docs/var_analysis.png for the visualization")
print("2. Run 'git add .' to stage changes")
print("3. Run 'git commit -m \"Add VaR visualization\"'")
print("4. Run 'git push origin main' to upload")
