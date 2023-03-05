import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import sankey
import network
import volume

DEX_FEE = 0.003

def lower_profit_deviation(S: float, fee: float):
    return S * ((1 - fee)**2)
    
def upper_profit_deviation(S: float, fee: float):
    return S / ((1 - fee)**2)

def get_transaction_rounds_of(sender: str, df):
    sender_transaction_rounds = df.loc[df['sender'] == sender, 'round'].tolist()
    return sender_transaction_rounds

def get_color_list(n):
    colors = [
    'red',
    'blue',
    'green',
    'orange',
    'purple',
    'yellow',
    'cyan',
    'magenta',
    'black',
    'white',
    'gray',
    'pink',
    'brown',
    'olive',
    'navy',
    'teal'
    ]
    return colors[:n]

def get_max_price(df):
    max_price = df[[
        'HUMBLESWAP_ALGOUSDC',
        'HUMBLESWAP_ALGOUSDT',
        'HUMBLESWAP_ALGOgoUSD',
        'PACT_ALGOUSDC',
        'PACT_ALGOUSDT',
        'TINYMAN(v1.1)_ALGOUSDC',
        'TINYMAN(v1.1)_ALGOUSDT'
    ]].max().max()
    return max_price

def get_min_price(df):
    min_price = df[[
        'HUMBLESWAP_ALGOUSDC',
        'HUMBLESWAP_ALGOUSDT',
        'HUMBLESWAP_ALGOgoUSD',
        'PACT_ALGOUSDC',
        'PACT_ALGOUSDT',
        'TINYMAN(v1.1)_ALGOUSDC',
        'TINYMAN(v1.1)_ALGOUSDT'
    ]].min().min()
    return min_price

def create_price_chart(df_prices, df_txs, addresses = None):
    df_prices['lower_profit_deviation'] = lower_profit_deviation(df_prices['Binance_ALGOUSDT'], DEX_FEE)
    df_prices['upper_profit_deviation'] = upper_profit_deviation(df_prices['Binance_ALGOUSDT'], DEX_FEE)

    fig = px.line(
        df_prices,
        x = 'round',
        y = [
            'Binance_ALGOUSDT',
            'HUMBLESWAP_ALGOUSDC',
            'HUMBLESWAP_ALGOUSDT',
            'HUMBLESWAP_ALGOgoUSD',
            'PACT_ALGOUSDC',
            'PACT_ALGOUSDT',
            'TINYMAN(v1.1)_ALGOUSDC',
            'TINYMAN(v1.1)_ALGOUSDT'
        ],
        title = "Price Data",
        line_shape = 'hv'
    )

    fig.add_scatter(
        x=df_prices['round'],
        y=df_prices['upper_profit_deviation'],
        mode='lines',
        line=dict(width=0.5, color='lightblue'),
        showlegend=False)
    fig.add_scatter(
        x=df_prices['round'],
        y=df_prices['lower_profit_deviation'],
        mode='lines',
        line=dict(width=0.5, color='lightblue'),
        showlegend=False)
    
    addresses = addresses.keys()
    if addresses.any():
        
        options = st.multiselect(
                'Senders to monitor.',
                addresses,
                [])
        colors = get_color_list(len(options))
        for address, color in zip(options, colors):
            rounds_list = get_transaction_rounds_of(address, df_txs)
            for round_ in rounds_list:
                fig.add_shape(
                    type = "line",
                    x0 = round_,
                    y0 = get_min_price(df_prices),
                    x1=round_,
                    y1 = get_max_price(df_prices),
                    line = dict(
                        color=color,
                        width=0.5,
                        dash="solid",
                    )
                )
                
    fig.update_layout(
        xaxis=dict(
            title="Block-Number",
            showgrid=True,
            gridwidth=0.05,
            dtick=200,
            tickformat='.0f'),
        yaxis=dict(
            title_text="Prices"),
    )

    fig.update_layout(
        plot_bgcolor='rgba(50,50,50,0)', # make plot background transparent
        paper_bgcolor='rgba(50,50,50,0)', # make paper background transparent
        xaxis=dict(gridcolor='rgba(100,100,100,0.5)', gridwidth=0.1),
        yaxis=dict(gridcolor='rgba(100,100,100,0.5)', gridwidth=0.1)
    )

    return fig


def delete_outside_transactions(transactions):
    markets = pd.read_csv("./data/markets.csv")
    market_addresses = markets['address'].tolist()
    transactions = transactions[transactions['receiver'].isin(market_addresses)]
    return transactions

def simplyfy_prices_dataframe(df_prices):
    redundant_columns = [
    'round:.2',
    'round:.3',
    'round:.4',
    'round:.5',
    'round:.6',
    ]
    df_prices = df_prices.drop(columns=redundant_columns)
    df_prices = df_prices.rename(columns={'round:': 'round'})
    return df_prices

def get_n_biggest_senders(df_txs, n):
    sender_counts = df_txs.groupby('sender')['sender'].count().sort_values(ascending=False)
    return sender_counts[:n]

def get_max_min_rounds(df):
    max_round = df['round'].max()
    min_round = df['round'].min()
    return min_round, max_round

def get_rounds_between(df, start_round, end_round):
    return df.loc[(df['round'] >= start_round) & (df['round'] <= end_round)]

def main():
    st.set_page_config(page_title='Algorand Analytics', layout = 'wide', page_icon = './images/logo.jpg')
    st.title("Algorand Analytics")

    #option = st.selectbox(
    #'Which dataset you want to analyze?',
    #('27410001', '27132402'))

    TRANSACTION_FILE = f'./data/transactions_27410001.csv'
    PRICE_HISTORY_FILE = f'./data/responses_27410001.csv'

    transactions = pd.read_csv(TRANSACTION_FILE)
    prices = pd.read_csv(PRICE_HISTORY_FILE)

    prices = simplyfy_prices_dataframe(prices)
    transactions = delete_outside_transactions(transactions)

    #min_round, max_round = get_max_min_rounds(transactions)
    #start_round, end_round = st.select_slider(
    #    'Select a rounds you want to display',
    #    options=transactions[['round']],
    #    value=(min_round, max_round))
    #transactions = get_rounds_between(transactions, start_round, end_round)

    biggest_senders_list = get_n_biggest_senders(transactions, 10)

    chart_fig = create_price_chart(prices, transactions, biggest_senders_list)
    st.plotly_chart(chart_fig, use_container_width=True)

    sankey_fig = sankey.create_sankey_graph(transactions, 100)
    st.plotly_chart(sankey_fig, use_container_width=True)

    network_fig = network.create_network_graph(transactions)
    st.plotly_chart(network_fig, use_container_width=True)

    #volume_fig = volume.plot_volume_trades(transactions)
    #st.plotly_chart(volume_fig, use_container_width=True)

    st.json(transactions.to_dict(), expanded=False)

if __name__ == "__main__":
    main()
