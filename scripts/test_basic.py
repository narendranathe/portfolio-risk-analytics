"""
Basic system test to verify everything works
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))


def test_market_data():
    print("🧪 Testing Market Data Simulator...")
    from data_ingestion.market_data_simulator import MarketDataSimulator
    
    simulator = MarketDataSimulator()
    tick = simulator.generate_tick('AAPL')
    
    assert tick.symbol == 'AAPL'
    assert tick.price > 0
    assert tick.volume > 0
    
    print("✅ Market data simulator works!")


def test_var_calculator():
    print("🧪 Testing VaR Calculator...")
    from risk_engine.simple_var import SimpleVaRCalculator
    import numpy as np
    
    calculator = SimpleVaRCalculator()
    returns = np.random.normal(0, 0.01, 100).tolist()
    results = calculator.calculate_var(returns, 1000000)
    
    assert 'var_amount' in results
    assert results['var_amount'] > 0
    
    print("✅ VaR calculator works!")


def test_imports():
    print("🧪 Testing Python imports...")
    
    try:
        import numpy
        import pandas
        print("✅ Core packages imported successfully!")
        return True
    except ImportError as e:
        print(f"⚠️  Import error: {e}")
        return False


if __name__ == "__main__":
    print("=" * 80)
    print("PORTFOLIO RISK ANALYTICS - BASIC TESTS")
    print("=" * 80)
    print()
    
    try:
        if not test_imports():
            print("Install missing packages with: conda install numpy pandas")
            sys.exit(1)
        
        print()
        test_market_data()
        print()
        test_var_calculator()
        print()
        print("=" * 80)
        print("🎉 ALL BASIC TESTS PASSED!")
        print("=" * 80)
    
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
