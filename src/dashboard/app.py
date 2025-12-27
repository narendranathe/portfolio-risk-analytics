"""
PROFESSIONAL PORTFOLIO RISK ANALYTICS DASHBOARD
Advanced risk metrics, actionable insights, and beautiful visualizations
"""

import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import time

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Portfolio Risk Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_BASE_URL = "http://localhost:8000"

# ============================================================================
# ADVANCED STYLING
# ============================================================================

st.markdown("""
<style>
    /* Main Background */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom Header */
    .dashboard-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
        animation: fadeIn 1s ease-in;
    }
    
    .dashboard-title {
        font-size: 3.5rem;
        font-weight: 900;
        margin: 0;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
        letter-spacing: -1px;
    }
    
    .dashboard-subtitle {
        font-size: 1.3rem;
        opacity: 0.95;
        margin-top: 0.5rem;
        font-weight: 300;
    }
    
    /* Metric Cards */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        border-left: 5px solid #667eea;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 35px rgba(0,0,0,0.15);
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    div[data-testid="stMetricLabel"] {
        font-size: 0.95rem;
        color: #6c757d;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2d3748 0%, #1a202c 100%);
        padding: 2rem 1rem;
    }
    
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] .stRadio label {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        transition: all 0.3s;
    }
    
    section[data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(102, 126, 234, 0.3);
        transform: translateX(5px);
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        border: none;
        font-weight: 700;
        font-size: 1rem;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.6);
    }
    
    /* Info/Warning/Error Boxes */
    .stAlert {
        border-radius: 15px;
        border-left: 5px solid;
        padding: 1.5rem;
        animation: slideIn 0.5s ease;
    }
    
    /* Download Button */
    .stDownloadButton button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        border: none;
        font-weight: 700;
        box-shadow: 0 6px 20px rgba(245, 87, 108, 0.4);
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #2d3748;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #667eea;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA FUNCTIONS
# ============================================================================

def get_portfolio_data():
    """Get portfolio VaR data"""
    try:
        response = requests.get(f"{API_BASE_URL}/portfolio/var", timeout=3)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def calculate_advanced_metrics(df):
    """Calculate advanced risk metrics"""
    metrics = {}
    
    # Portfolio metrics
    metrics['total_var_95'] = df['var_95'].sum()
    metrics['total_var_99'] = df['var_99'].sum()
    metrics['avg_var_95'] = df['var_95'].mean()
    metrics['portfolio_value'] = df['current_price'].sum()
    
    # Risk concentration
    df['weight'] = df['current_price'] / df['current_price'].sum()
    metrics['concentration_index'] = (df['weight'] ** 2).sum()  # Herfindahl Index
    
    # Risk-adjusted metrics
    df['risk_pct'] = (df['var_95'] / df['current_price']) * 100
    metrics['avg_risk_pct'] = df['risk_pct'].mean()
    metrics['max_risk_pct'] = df['risk_pct'].max()
    metrics['min_risk_pct'] = df['risk_pct'].min()
    
    # Portfolio risk score (0-100)
    risk_score = min(100, metrics['avg_risk_pct'] * 10)
    metrics['risk_score'] = risk_score
    
    # Diversification benefit
    individual_var_sum = df['var_95'].sum()
    portfolio_var = np.sqrt((df['var_95'] ** 2).sum())  # Simplified portfolio VaR
    metrics['diversification_benefit'] = ((individual_var_sum - portfolio_var) / individual_var_sum) * 100
    
    return metrics

def get_risk_recommendations(metrics, df):
    """Generate actionable recommendations"""
    recommendations = []
    
    # High concentration risk
    if metrics['concentration_index'] > 0.3:
        recommendations.append({
            'type': 'warning',
            'title': '⚠️ High Concentration Risk',
            'message': f"Portfolio is concentrated (HHI: {metrics['concentration_index']:.2f}). Consider diversifying across more positions.",
            'action': 'Reduce position sizes in top holdings'
        })
    
    # High VaR positions
    high_risk_symbols = df[df['risk_pct'] > 7]['symbol'].tolist()
    if high_risk_symbols:
        recommendations.append({
            'type': 'error',
            'title': '🔴 High Risk Positions',
            'message': f"These symbols have VaR >7%: {', '.join(high_risk_symbols)}",
            'action': 'Review and consider reducing exposure or hedging'
        })
    
    # Portfolio risk score
    if metrics['risk_score'] > 70:
        recommendations.append({
            'type': 'error',
            'title': '🚨 High Portfolio Risk',
            'message': f"Overall risk score is {metrics['risk_score']:.0f}/100",
            'action': 'Implement risk reduction strategy immediately'
        })
    elif metrics['risk_score'] > 40:
        recommendations.append({
            'type': 'warning',
            'title': '⚠️ Moderate Portfolio Risk',
            'message': f"Risk score is {metrics['risk_score']:.0f}/100",
            'action': 'Monitor closely and prepare contingency plans'
        })
    else:
        recommendations.append({
            'type': 'success',
            'title': '✅ Healthy Risk Profile',
            'message': f"Risk score is {metrics['risk_score']:.0f}/100",
            'action': 'Maintain current risk management practices'
        })
    
    # Diversification
    if metrics['diversification_benefit'] < 10:
        recommendations.append({
            'type': 'warning',
            'title': '📉 Low Diversification',
            'message': f"Only {metrics['diversification_benefit']:.1f}% benefit from diversification",
            'action': 'Add uncorrelated assets to improve diversification'
        })
    else:
        recommendations.append({
            'type': 'success',
            'title': '✅ Good Diversification',
            'message': f"Achieving {metrics['diversification_benefit']:.1f}% diversification benefit",
            'action': 'Continue maintaining balanced portfolio'
        })
    
    return recommendations

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    # Sidebar
    with st.sidebar:
        st.markdown("## 🎯 NAVIGATION")
        st.markdown("---")
        
        page = st.radio(
            "Select View",
            ["📊 Executive Dashboard", "🔍 Deep Dive Analysis", "⚡ Risk Alerts", "📈 Portfolio Optimizer"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("### ⚙️ CONTROLS")
        
        auto_refresh = st.checkbox("🔄 Auto-refresh (5s)", value=False)
        
        if st.button("♻️ REFRESH NOW"):
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📡 STATUS")
        st.caption(f"🕐 {datetime.now().strftime('%H:%M:%S')}")
        
        # Check API status
        try:
            response = requests.get(f"{API_BASE_URL}/status", timeout=2)
            if response.status_code == 200:
                st.success("✅ API Connected")
            else:
                st.error("⚠️ API Error")
        except:
            st.error("❌ API Offline")
    
    # Route to pages
    if page == "📊 Executive Dashboard":
        show_executive_dashboard()
    elif page == "🔍 Deep Dive Analysis":
        show_deep_dive()
    elif page == "⚡ Risk Alerts":
        show_risk_alerts()
    else:
        show_portfolio_optimizer()
    
    # Auto-refresh
    if auto_refresh:
        time.sleep(5)
        st.rerun()

# ============================================================================
# EXECUTIVE DASHBOARD
# ============================================================================

def show_executive_dashboard():
    """Executive-level portfolio overview with actionable insights"""
    
    # Header
    st.markdown("""
    <div class="dashboard-header">
        <h1 class="dashboard-title">📊 PORTFOLIO RISK ANALYTICS</h1>
        <p class="dashboard-subtitle">Real-time Risk Intelligence & Decision Support</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get data
    data = get_portfolio_data()
    
    if not data or 'results' not in data:
        st.error("❌ **API Connection Failed**")
        st.code("python src/api/main.py", language="bash")
        st.stop()
    
    df = pd.DataFrame(data['results'])
    metrics = calculate_advanced_metrics(df)
    
    # ========== KEY METRICS ROW ==========
    st.markdown('<p class="section-header">🎯 KEY PERFORMANCE INDICATORS</p>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "Portfolio Value",
            f"${metrics['portfolio_value']:.2f}",
            delta="Total Exposure"
        )
    
    with col2:
        st.metric(
            "Total VaR (95%)",
            f"${metrics['total_var_95']:.2f}",
            delta=f"{(metrics['total_var_95']/metrics['portfolio_value']*100):.1f}%"
        )
    
    with col3:
        risk_color = "🟢" if metrics['risk_score'] < 40 else "🟡" if metrics['risk_score'] < 70 else "🔴"
        st.metric(
            "Risk Score",
            f"{risk_color} {metrics['risk_score']:.0f}/100",
            delta="Composite Risk"
        )
    
    with col4:
        st.metric(
            "Diversification",
            f"{metrics['diversification_benefit']:.1f}%",
            delta="Benefit"
        )
    
    with col5:
        concentration_status = "Low" if metrics['concentration_index'] < 0.2 else "Med" if metrics['concentration_index'] < 0.3 else "High"
        st.metric(
            "Concentration",
            concentration_status,
            delta=f"HHI: {metrics['concentration_index']:.2f}"
        )
    
    st.markdown("---")
    
    # ========== RISK ALERTS ==========
    recommendations = get_risk_recommendations(metrics, df)
    
    st.markdown('<p class="section-header">⚡ ACTIONABLE INSIGHTS</p>', unsafe_allow_html=True)
    
    cols = st.columns(len(recommendations))
    for idx, rec in enumerate(recommendations):
        with cols[idx]:
            if rec['type'] == 'error':
                st.error(f"**{rec['title']}**\n\n{rec['message']}\n\n💡 *Action: {rec['action']}*")
            elif rec['type'] == 'warning':
                st.warning(f"**{rec['title']}**\n\n{rec['message']}\n\n💡 *Action: {rec['action']}*")
            else:
                st.success(f"**{rec['title']}**\n\n{rec['message']}\n\n💡 *Action: {rec['action']}*")
    
    st.markdown("---")
    
    # ========== VISUALIZATIONS ==========
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<p class="section-header">📊 Risk Distribution Analysis</p>', unsafe_allow_html=True)
        
        # Create sophisticated bar chart with annotations
        df_sorted = df.sort_values('var_95', ascending=False)
        
        fig = go.Figure()
        
        # Add bars with gradient colors
        colors = ['#e74c3c' if x > 7 else '#f39c12' if x > 5 else '#27ae60' 
                  for x in df_sorted['risk_pct']]
        
        fig.add_trace(go.Bar(
            y=df_sorted['symbol'],
            x=df_sorted['var_95'],
            orientation='h',
            marker=dict(
                color=colors,
                line=dict(color='rgba(0,0,0,0.3)', width=2)
            ),
            text=[f'${x:.2f}' for x in df_sorted['var_95']],
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>VaR 95%%: $%{x:.2f}<br>Risk: %{customdata:.2f}%<extra></extra>',
            customdata=df_sorted['risk_pct']
        ))
        
        fig.update_layout(
            height=400,
            xaxis_title="Value at Risk (95% Confidence)",
            yaxis_title="Symbol",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12, color='#2d3748'),
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<p class="section-header">📈 Confidence Level Comparison</p>', unsafe_allow_html=True)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='95% Confidence',
            x=df['symbol'],
            y=df['var_95'],
            marker=dict(
                color='#667eea',
                line=dict(color='rgba(0,0,0,0.3)', width=2)
            ),
            hovertemplate='<b>%{x}</b><br>VaR 95%%: $%{y:.2f}<extra></extra>'
        ))
        
        fig.add_trace(go.Bar(
            name='99% Confidence',
            x=df['symbol'],
            y=df['var_99'],
            marker=dict(
                color='#764ba2',
                line=dict(color='rgba(0,0,0,0.3)', width=2)
            ),
            hovertemplate='<b>%{x}</b><br>VaR 99%%: $%{y:.2f}<extra></extra>'
        ))
        
        fig.update_layout(
            height=400,
            barmode='group',
            xaxis_title="Symbol",
            yaxis_title="Value at Risk ($)",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12, color='#2d3748'),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            margin=dict(l=20, r=20, t=40, b=20),
            yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # ========== PORTFOLIO COMPOSITION ==========
    st.markdown('<p class="section-header">🎯 Portfolio Composition & Risk Mapping</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Portfolio allocation pie chart
        fig = go.Figure(data=[go.Pie(
            labels=df['symbol'],
            values=df['current_price'],
            hole=.4,
            marker=dict(
                colors=['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe'],
                line=dict(color='white', width=3)
            ),
            textinfo='label+percent',
            textfont=dict(size=14, color='white'),
            hovertemplate='<b>%{label}</b><br>Value: $%{value:.2f}<br>Share: %{percent}<extra></extra>'
        )])
        
        fig.update_layout(
            height=400,
            title=dict(text="Portfolio Allocation", font=dict(size=16, color='#2d3748')),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=50, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Risk heatmap
        fig = px.treemap(
            df,
            path=['symbol'],
            values='current_price',
            color='risk_pct',
            color_continuous_scale='RdYlGn_r',
            title='Risk Heatmap (Size = Exposure, Color = Risk %)',
            hover_data={'current_price': ':$.2f', 'risk_pct': ':.2f%', 'var_95': ':$.2f'}
        )
        
        fig.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=50, b=20),
            font=dict(size=12, color='#2d3748')
        )
        
        fig.update_traces(
            textinfo="label+value",
            textfont=dict(size=14, color='white'),
            marker=dict(line=dict(color='white', width=3))
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # ========== DETAILED DATA TABLE ==========
    st.markdown('<p class="section-header">📋 Detailed Risk Analytics</p>', unsafe_allow_html=True)
    
    # Prepare display dataframe
    display_df = df.copy()
    display_df['weight'] = (display_df['current_price'] / display_df['current_price'].sum() * 100)
    display_df['risk_pct'] = (display_df['var_95'] / display_df['current_price'] * 100)
    display_df['risk_status'] = display_df['risk_pct'].apply(
        lambda x: '🟢 Low' if x < 5 else '🟡 Medium' if x < 7 else '🔴 High'
    )
    
    display_df = display_df[['symbol', 'current_price', 'weight', 'var_95', 'var_99', 'risk_pct', 'risk_status', 'num_observations']]
    display_df.columns = ['Symbol', 'Position Value', 'Weight (%)', 'VaR 95%', 'VaR 99%', 'Risk %', 'Status', 'Data Points']
    
    # Format numbers
    display_df['Position Value'] = display_df['Position Value'].apply(lambda x: f'${x:.2f}')
    display_df['Weight (%)'] = display_df['Weight (%)'].apply(lambda x: f'{x:.1f}%')
    display_df['VaR 95%'] = display_df['VaR 95%'].apply(lambda x: f'${x:.2f}')
    display_df['VaR 99%'] = display_df['VaR 99%'].apply(lambda x: f'${x:.2f}')
    display_df['Risk %'] = display_df['Risk %'].apply(lambda x: f'{x:.2f}%')
    
    st.dataframe(
        display_df,
        hide_index=True,
        height=300
    )
    
    # Download button
    csv = df.to_csv(index=False)
    st.download_button(
        "📥 DOWNLOAD FULL REPORT",
        csv,
        f"portfolio_risk_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        "text/csv",
        key='download-csv'
    )

# ============================================================================
# DEEP DIVE ANALYSIS
# ============================================================================

def show_deep_dive():
    """Detailed symbol-level analysis"""
    
    st.markdown("""
    <div class="dashboard-header">
        <h1 class="dashboard-title">🔍 DEEP DIVE ANALYSIS</h1>
        <p class="dashboard-subtitle">Symbol-Level Risk Intelligence</p>
    </div>
    """, unsafe_allow_html=True)
    
    data = get_portfolio_data()
    if not data or 'results' not in data:
        st.error("❌ Cannot load data")
        st.stop()
    
    df = pd.DataFrame(data['results'])
    
    # Symbol selector
    selected = st.selectbox("🎯 Select Symbol for Analysis", df['symbol'].tolist(), index=0)
    
    symbol_data = df[df['symbol'] == selected].iloc[0]
    
    # Metrics row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Symbol", symbol_data['symbol'])
    
    with col2:
        st.metric("Position Value", f"${symbol_data['current_price']:.2f}")
    
    with col3:
        st.metric("VaR 95%", f"${symbol_data['var_95']:.2f}")
    
    with col4:
        st.metric("VaR 99%", f"${symbol_data['var_99']:.2f}")
    
    with col5:
        risk_pct = (symbol_data['var_95'] / symbol_data['current_price']) * 100
        st.metric("Risk %", f"{risk_pct:.2f}%")
    
    st.markdown("---")
    
    # Risk gauge and analysis
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<p class="section-header">🎯 Risk Gauge</p>', unsafe_allow_html=True)
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=risk_pct,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Risk Level (%)", 'font': {'size': 24}},
            delta={'reference': 5, 'increasing': {'color': "red"}, 'decreasing': {'color': "green"}},
            gauge={
                'axis': {'range': [None, 15], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "#667eea", 'thickness': 0.75},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 3], 'color': '#d4edda'},
                    {'range': [3, 7], 'color': '#fff3cd'},
                    {'range': [7, 15], 'color': '#f8d7da'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 10
                }
            }
        ))
        
        fig.update_layout(
            height=350,
            margin=dict(l=20, r=20, t=50, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            font={'color': "#2d3748", 'family': "Arial"}
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<p class="section-header">📊 Risk Breakdown</p>', unsafe_allow_html=True)
        
        # Create risk comparison chart
        fig = go.Figure()
        
        categories = ['VaR 95%', 'VaR 99%', 'Position Value']
        values = [symbol_data['var_95'], symbol_data['var_99'], symbol_data['current_price']]
        colors = ['#667eea', '#764ba2', '#4facfe']
        
        fig.add_trace(go.Bar(
            x=categories,
            y=values,
            marker=dict(color=colors, line=dict(color='rgba(0,0,0,0.3)', width=2)),
            text=[f'${v:.2f}' for v in values],
            textposition='outside'
        ))
        
        fig.update_layout(
            height=350,
            yaxis_title="Amount ($)",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=20, b=20),
            font=dict(size=12, color='#2d3748'),
            yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed analysis
    st.markdown('<p class="section-header">📈 Detailed Analysis</p>', unsafe_allow_html=True)
    
    risk_level = "🟢 LOW RISK" if risk_pct < 5 else "🟡 MODERATE RISK" if risk_pct < 7 else "🔴 HIGH RISK"
    
    portfolio_weight = (symbol_data['current_price'] / df['current_price'].sum()) * 100
    
    analysis_text = f"""
    ### {selected} - Risk Assessment
    
    **Overall Risk Classification:** {risk_level}
    
    **Key Metrics:**
    - Current Position: ${symbol_data['current_price']:.2f}
    - Portfolio Weight: {portfolio_weight:.2f}%
    - Value at Risk (95% confidence): ${symbol_data['var_95']:.2f} ({risk_pct:.2f}%)
    - Value at Risk (99% confidence): ${symbol_data['var_99']:.2f}
    - Historical Data Points: {symbol_data['num_observations']}
    
    **Interpretation:**
    - With 95% confidence, the maximum expected loss over the holding period is **${symbol_data['var_95']:.2f}**
    - There is a 5% chance that losses could exceed this amount
    - The extreme VaR (99% confidence) is **${symbol_data['var_99']:.2f}**
    
    **Recommendations:**
    """
    
    if risk_pct > 7:
        analysis_text += """
    - ⚠️ **HIGH RISK ALERT**: Consider reducing position size
    - 🛡️ Consider hedging strategies (options, stops)
    - 📊 Review correlation with other portfolio holdings
    - ⏰ Increase monitoring frequency
    """
    elif risk_pct > 5:
        analysis_text += """
    - 📊 **MODERATE RISK**: Monitor closely
    - 🎯 Consider setting stop-loss levels
    - 📈 Review position sizing in context of overall portfolio
    - ⚖️ Evaluate risk-reward ratio
    """
    else:
        analysis_text += """
    - ✅ **ACCEPTABLE RISK**: Within normal parameters
    - 📊 Continue regular monitoring
    - 🎯 Maintain current position or consider increasing if opportunity presents
    - 📈 Risk profile aligns with conservative strategy
    """
    
    st.info(analysis_text)

# ============================================================================
# RISK ALERTS
# ============================================================================

def show_risk_alerts():
    """Risk monitoring and alert system"""
    
    st.markdown("""
    <div class="dashboard-header">
        <h1 class="dashboard-title">⚡ RISK ALERT SYSTEM</h1>
        <p class="dashboard-subtitle">Real-time Risk Monitoring & Alerts</p>
    </div>
    """, unsafe_allow_html=True)
    
    data = get_portfolio_data()
    if not data or 'results' not in data:
        st.error("❌ Cannot load data")
        st.stop()
    
    df = pd.DataFrame(data['results'])
    metrics = calculate_advanced_metrics(df)
    recommendations = get_risk_recommendations(metrics, df)
    
    # Alert summary
    col1, col2, col3 = st.columns(3)
    
    critical_count = sum(1 for r in recommendations if r['type'] == 'error')
    warning_count = sum(1 for r in recommendations if r['type'] == 'warning')
    ok_count = sum(1 for r in recommendations if r['type'] == 'success')
    
    with col1:
        st.metric("🔴 Critical Alerts", critical_count)
    with col2:
        st.metric("🟡 Warnings", warning_count)
    with col3:
        st.metric("🟢 All Clear", ok_count)
    
    st.markdown("---")
    
    # Display all recommendations
    for rec in recommendations:
        if rec['type'] == 'error':
            st.error(f"""
            ### {rec['title']}
            
            **Issue:** {rec['message']}
            
            **Recommended Action:** {rec['action']}
            """)
        elif rec['type'] == 'warning':
            st.warning(f"""
            ### {rec['title']}
            
            **Issue:** {rec['message']}
            
            **Recommended Action:** {rec['action']}
            """)
        else:
            st.success(f"""
            ### {rec['title']}
            
            **Status:** {rec['message']}
            
            **Recommendation:** {rec['action']}
            """)

# ============================================================================
# PORTFOLIO OPTIMIZER
# ============================================================================

def show_portfolio_optimizer():
    """Portfolio optimization recommendations"""
    
    st.markdown("""
    <div class="dashboard-header">
        <h1 class="dashboard-title">📈 PORTFOLIO OPTIMIZER</h1>
        <p class="dashboard-subtitle">Risk-Adjusted Portfolio Recommendations</p>
    </div>
    """, unsafe_allow_html=True)
    
    data = get_portfolio_data()
    if not data or 'results' not in data:
        st.error("❌ Cannot load data")
        st.stop()
    
    df = pd.DataFrame(data['results'])
    metrics = calculate_advanced_metrics(df)
    
    st.markdown('<p class="section-header">🎯 Optimization Goals</p>', unsafe_allow_html=True)
    
    target_risk = st.slider("Target Portfolio Risk Score (0-100)", 0, 100, 40)
    
    st.markdown("---")
    
    # Current vs Target
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Current Risk Score", f"{metrics['risk_score']:.0f}")
    with col2:
        st.metric("Target Risk Score", f"{target_risk:.0f}")
    with col3:
        delta = metrics['risk_score'] - target_risk
        st.metric("Gap", f"{delta:+.0f}", delta=f"{'Reduce' if delta > 0 else 'Room to Grow'}")
    
    st.markdown("---")
    
    # Recommendations
    st.markdown('<p class="section-header">💡 Optimization Recommendations</p>', unsafe_allow_html=True)
    
    if metrics['risk_score'] > target_risk:
        st.warning(f"""
        ### 📉 Risk Reduction Strategy Required
        
        Your current portfolio risk ({metrics['risk_score']:.0f}/100) exceeds your target ({target_risk}/100).
        
        **Recommended Actions:**
        1. **Reduce High-Risk Positions**: Consider trimming positions with VaR >7%
        2. **Increase Diversification**: Add low-correlation assets
        3. **Implement Hedging**: Use options or other derivatives
        4. **Rebalance**: Shift allocation toward lower-risk securities
        
        **Expected Impact:** Reducing risk score by {(metrics['risk_score'] - target_risk):.0f} points
        """)
    else:
        st.success(f"""
        ### ✅ Risk Target Achieved
        
        Your portfolio risk ({metrics['risk_score']:.0f}/100) is within your target ({target_risk}/100).
        
        **Opportunities:**
        1. **Maintain Current Strategy**: Continue monitoring
        2. **Consider Growth**: You have {(target_risk - metrics['risk_score']):.0f} points of risk capacity
        3. **Optimize Returns**: Look for risk-adjusted return improvements
        4. **Stay Balanced**: Maintain diversification benefits
        """)
    
    # Show rebalancing suggestions
    st.markdown('<p class="section-header">⚖️ Suggested Rebalancing</p>', unsafe_allow_html=True)
    
    # Calculate suggested weights
    df_rebal = df.copy()
    df_rebal['current_weight'] = df_rebal['current_price'] / df_rebal['current_price'].sum() * 100
    
    # Simple inverse risk weighting
    df_rebal['inv_risk'] = 1 / df_rebal['risk_pct']
    df_rebal['suggested_weight'] = df_rebal['inv_risk'] / df_rebal['inv_risk'].sum() * 100
    df_rebal['weight_change'] = df_rebal['suggested_weight'] - df_rebal['current_weight']
    
    # Display
    display_rebal = df_rebal[['symbol', 'current_weight', 'suggested_weight', 'weight_change']]
    display_rebal.columns = ['Symbol', 'Current %', 'Suggested %', 'Change']
    
    display_rebal['Current %'] = display_rebal['Current %'].apply(lambda x: f'{x:.1f}%')
    display_rebal['Suggested %'] = display_rebal['Suggested %'].apply(lambda x: f'{x:.1f}%')
    display_rebal['Change'] = display_rebal['Change'].apply(lambda x: f'{x:+.1f}%')
    
    st.dataframe(display_rebal, hide_index=True)

# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == "__main__":
    main()