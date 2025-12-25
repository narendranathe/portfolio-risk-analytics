#!/usr/bin/env python
# coding: utf-8

# # Portfolio Risk Analytics - VaR Analysis
# 
# ## Value at Risk Calculation and Visualization
# 
# This notebook demonstrates:
# - Historical VaR calculation
# - Monte Carlo simulation
# - Risk metric visualization
# - Portfolio stress testing
# 
# **Author:** Narendranath Edara  
# **Project:** Real-Time Portfolio Risk Analytics System  
# **GitHub:** [portfolio-risk-analytics](https://github.com/narendranathe/portfolio-risk-analytics)

# In[ ]:


import sys
sys.path.append('../src')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from risk_engine.simple_var import SimpleVaRCalculator

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette('husl')
get_ipython().run_line_magic('matplotlib', 'inline')

print("✅ Libraries imported successfully!")


# ## Generate Sample Portfolio Returns
# 
# We'll simulate 1 year (252 trading days) of daily returns with:
# - Mean daily return: 0.05%
# - Daily volatility: 1.5%
# - Portfolio value: $10,000,000

# In[ ]:


# Simulate 1 year of daily returns
np.random.seed(42)
returns = np.random.normal(0.0005, 0.015, 252)

# Portfolio value
portfolio_value = 10_000_000

# Convert to DataFrame
df_returns = pd.DataFrame({
    'date': pd.date_range(start='2024-01-01', periods=252, freq='B'),
    'daily_return': returns
})

df_returns['cumulative_return'] = (1 + df_returns['daily_return']).cumprod() - 1
df_returns['portfolio_value'] = portfolio_value * (1 + df_returns['cumulative_return'])

print(f"Generated {len(df_returns)} days of return data")
print(f"\nFirst 5 rows:")
df_returns.head()


# ## Calculate VaR Metrics
# 
# Using our custom VaR calculator to compute:
# - 95% Value at Risk (VaR)
# - Conditional VaR (CVaR / Expected Shortfall)
# - Return statistics

# In[ ]:


# Calculate VaR
var_calc = SimpleVaRCalculator(confidence_level=0.95)
var_results = var_calc.calculate_var(returns.tolist(), portfolio_value)

print('Portfolio Risk Metrics')
print('=' * 60)
print(f"Portfolio Value: ${var_results['portfolio_value']:,}")
print(f"Confidence Level: {var_results['confidence_level']*100}%")
print(f"\n📉 95% VaR: ${var_results['var_amount']:,}")
print(f"   In 95% of cases, daily loss will not exceed ${var_results['var_amount']:,}")
print(f"   ({var_results['var_percentage']}% of portfolio)")
print(f"\n📉 95% CVaR (Expected Shortfall): ${var_results['cvar_amount']:,}")
print(f"   If we exceed VaR, average loss is ${var_results['cvar_amount']:,}")
print(f"\n📊 Best Daily Return: +{var_results['best_return']}%")
print(f"📊 Worst Daily Return: {var_results['worst_return']}%")


# ## Visualize Portfolio Performance
# 
# Creating comprehensive visualizations:
# 1. Portfolio value over time
# 2. Returns distribution with VaR threshold
# 3. Cumulative returns
# 4. Tail risk analysis

# In[ ]:


fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 1. Portfolio Value Over Time
axes[0, 0].plot(df_returns['date'], df_returns['portfolio_value'], 
                linewidth=2.5, color='#2E86AB', label='Portfolio Value')
axes[0, 0].axhline(y=portfolio_value, color='#A23B72', linestyle='--', 
                   linewidth=2, label='Initial Value')
axes[0, 0].set_title('Portfolio Value Over Time', fontsize=16, fontweight='bold', pad=20)
axes[0, 0].set_xlabel('Date', fontsize=12)
axes[0, 0].set_ylabel('Portfolio Value ($)', fontsize=12)
axes[0, 0].legend(fontsize=10)
axes[0, 0].grid(True, alpha=0.3)
axes[0, 0].tick_params(axis='x', rotation=45)

# 2. Returns Distribution
axes[0, 1].hist(returns * 100, bins=40, edgecolor='black', alpha=0.7, 
                color='#F18F01', label='Daily Returns')
axes[0, 1].axvline(x=np.percentile(returns * 100, 5), color='#C73E1D', 
                   linestyle='--', linewidth=3, label=f'5th Percentile (VaR)')
axes[0, 1].set_title('Daily Returns Distribution', fontsize=16, fontweight='bold', pad=20)
axes[0, 1].set_xlabel('Daily Return (%)', fontsize=12)
axes[0, 1].set_ylabel('Frequency', fontsize=12)
axes[0, 1].legend(fontsize=10)
axes[0, 1].grid(True, alpha=0.3)

# 3. Cumulative Returns
axes[1, 0].plot(df_returns['date'], df_returns['cumulative_return'] * 100, 
                linewidth=2.5, color='#6A4C93')
axes[1, 0].fill_between(df_returns['date'], 0, df_returns['cumulative_return'] * 100, 
                        alpha=0.3, color='#6A4C93')
axes[1, 0].axhline(y=0, color='black', linestyle='-', linewidth=0.8)
axes[1, 0].set_title('Cumulative Returns', fontsize=16, fontweight='bold', pad=20)
axes[1, 0].set_xlabel('Date', fontsize=12)
axes[1, 0].set_ylabel('Cumulative Return (%)', fontsize=12)
axes[1, 0].grid(True, alpha=0.3)
axes[1, 0].tick_params(axis='x', rotation=45)

# 4. VaR Illustration (Tail Risk)
sorted_returns = np.sort(returns * 100)
var_threshold = np.percentile(returns * 100, 5)

axes[1, 1].hist(returns * 100, bins=40, edgecolor='black', alpha=0.5, 
                label='All Returns', color='#8B8C89')
axes[1, 1].hist(sorted_returns[sorted_returns <= var_threshold], bins=20, 
                color='#C73E1D', alpha=0.8, label='VaR Exceedances (Tail Risk)')
axes[1, 1].axvline(x=var_threshold, color='#A4161A', linestyle='--', 
                   linewidth=3, label=f'VaR Threshold ({var_threshold:.2f}%)')
axes[1, 1].set_title('VaR and Tail Risk Analysis', fontsize=16, fontweight='bold', pad=20)
axes[1, 1].set_xlabel('Daily Return (%)', fontsize=12)
axes[1, 1].set_ylabel('Frequency', fontsize=12)
axes[1, 1].legend(fontsize=10)
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('../docs/var_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

print('\n✅ Visualization saved to docs/var_analysis.png')


# ## Compare Different Confidence Levels
# 
# Analyzing VaR at 90%, 95%, and 99% confidence levels to understand tail risk.

# In[ ]:


# Calculate VaR at different confidence levels
confidence_levels = [0.90, 0.95, 0.99]
var_comparison = []

for cl in confidence_levels:
    calc = SimpleVaRCalculator(confidence_level=cl)
    result = calc.calculate_var(returns.tolist(), portfolio_value)
    var_comparison.append({
        'Confidence Level': f"{cl*100}%",
        'VaR ($)': f"${result['var_amount']:,.0f}",
        'VaR (%)': f"{result['var_percentage']:.2f}%",
        'CVaR ($)': f"${result['cvar_amount']:,.0f}"
    })

df_comparison = pd.DataFrame(var_comparison)

print('\n📊 VaR Comparison Across Confidence Levels')
print('=' * 70)
print(df_comparison.to_string(index=False))
print('\n')

# Visualize comparison
fig, ax = plt.subplots(figsize=(10, 6))

cl_labels = [f"{int(cl*100)}%" for cl in confidence_levels]
var_values = [SimpleVaRCalculator(cl).calculate_var(returns.tolist(), portfolio_value)['var_amount'] 
              for cl in confidence_levels]

bars = ax.bar(cl_labels, var_values, color=['#52B788', '#F18F01', '#C73E1D'], 
              edgecolor='black', linewidth=1.5, alpha=0.8)

ax.set_title('VaR at Different Confidence Levels', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Confidence Level', fontsize=12)
ax.set_ylabel('Value at Risk ($)', fontsize=12)
ax.grid(True, alpha=0.3, axis='y')

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'${height:,.0f}',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.show()


# In[ ]:


# Calculate additional statistics
print('📊 Portfolio Statistics Summary')
print('=' * 70)
print(f"\nReturn Metrics:")
print(f"  Mean Daily Return: {returns.mean()*100:.4f}%")
print(f"  Daily Volatility: {returns.std()*100:.4f}%")
print(f"  Annualized Return: {returns.mean()*252*100:.2f}%")
print(f"  Annualized Volatility: {returns.std()*np.sqrt(252)*100:.2f}%")

print(f"\nRisk Metrics:")
print(f"  Sharpe Ratio (assuming 5% risk-free): {(returns.mean()*252 - 0.05)/(returns.std()*np.sqrt(252)):.3f}")
print(f"  Skewness: {pd.Series(returns).skew():.3f}")
print(f"  Kurtosis: {pd.Series(returns).kurtosis():.3f}")

print(f"\nPercentile Analysis:")
for p in [1, 5, 10, 90, 95, 99]:
    print(f"  {p}th Percentile: {np.percentile(returns*100, p):.3f}%")


# ## Key Takeaways
# 
# ### VaR Interpretation
# - **95% VaR**: With 95% confidence, daily losses should not exceed the calculated VaR amount
# - This means in only 5% of trading days (roughly 12-13 days per year), losses could exceed VaR
# 
# ### CVaR (Expected Shortfall)
# - Provides the average loss when VaR is breached
# - More informative than VaR alone as it captures tail risk severity
# 
# ### Portfolio Performance
# - Annualized return calculated from daily returns
# - Volatility indicates the portfolio's risk level
# - Sharpe ratio measures risk-adjusted returns
# 
# ### Risk Assessment
# - Portfolio shows normal distribution characteristics
# - Tail risk is captured in the CVaR metric
# - Higher confidence levels show exponentially larger VaR values
# 
# ## Next Steps for Enhancement
# 
# 1. ✅ Implement parametric VaR (assumes normal distribution)
# 2. ✅ Add Monte Carlo simulation VaR
# 3. ✅ Include correlation analysis between assets
# 4. ✅ Develop stress testing scenarios (2008 crisis, COVID crash)
# 5. ✅ Add backtesting framework to validate VaR accuracy
# 6. ✅ Implement Expected Shortfall at multiple confidence levels
# 7. ✅ Create portfolio optimization using VaR constraints
# 
# ---
# 
# **Project Repository:** [github.com/narendranathe/portfolio-risk-analytics](https://github.com/narendranathe/portfolio-risk-analytics)
