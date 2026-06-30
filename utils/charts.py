import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def plot_fraud_distribution(df):
    """Pie chart of Fraud vs Clean claims."""
    status_counts = df['Status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']
    fig = px.pie(status_counts, names='Status', values='Count', 
                 title='Fraud vs Clean Distribution',
                 color='Status', 
                 color_discrete_map={'Suspected Fraud':'red', 'Clean':'green'})
    return fig

def plot_claims_by_state(df):
    """Bar chart of claims by state."""
    state_counts = df.groupby(['State', 'Status']).size().unstack(fill_value=0).reset_index()
    fig = px.bar(state_counts, x='State', y=['Clean', 'Suspected Fraud'], 
                 title='Claims by State', barmode='stack',
                 color_discrete_map={'Clean': 'green', 'Suspected Fraud': 'red'})
    return fig

def plot_claim_amount_histogram(df):
    """Histogram of claim amounts by status."""
    fig = px.histogram(df, x='Claim_Amount', color='Status', 
                       nbins=50, title='Claim Amount Distribution',
                       color_discrete_map={'Clean': 'green', 'Suspected Fraud': 'red'},
                       marginal="box")
    return fig

def plot_monthly_trend(df):
    """Line chart showing monthly fraud vs clean trends."""
    df_copy = df.copy()
    df_copy['MonthYear'] = pd.to_datetime(df_copy['Date']).dt.to_period('M')
    trend = df_copy.groupby(['MonthYear', 'Status']).size().unstack(fill_value=0).reset_index()
    trend['MonthYear'] = trend['MonthYear'].astype(str)
    
    fig = px.line(trend, x='MonthYear', y=['Clean', 'Suspected Fraud'], 
                  title='Monthly Claim Trend', markers=True,
                  color_discrete_map={'Clean': 'green', 'Suspected Fraud': 'red'})
    return fig
