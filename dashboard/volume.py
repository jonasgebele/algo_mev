import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def plot_volume_trades(trades_df, round_size=100):
    # Convert the amount_send column to USD
    trades_df['amount_send'] = trades_df.apply(convert_amount_send, axis=1)

    # Convert the round column to integers and group them into bins
    trades_df['round_bin'] = pd.cut(trades_df['round'].astype(int), bins=range(0, trades_df['round'].max()+round_size, round_size))

    # Group the data by exchange and round_bin, and calculate the sum of amount_send
    grouped = trades_df.groupby(['receiver', 'round_bin'])['amount_send'].sum().reset_index()

    # Create a stacked bar chart using Plotly
    fig = px.bar(grouped, x='round_bin', y='amount_send', color='receiver', barmode='stack')

    # Set the title and axis labels
    fig.update_layout(title='Volume of Trades by Exchange Over Time', xaxis_title='Round', yaxis_title='Volume (USD)', yaxis_type='log')

    # Format the x-axis tick labels as integers
    fig.update_xaxes(type='category', tickmode='linear', tickvals=fig.data[0]['x'], ticktext=[int(round.left) for round in grouped['round_bin']])

    # Return the chart object
    return fig

def convert_amount_send(row):
    ALGO_PRICE = 0.25
    if row['asset_id_send'] == 0:
        return row['amount_send'] * ALGO_PRICE / 1000000
    else:
        return row['amount_send'] / 1000000