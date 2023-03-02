import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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

def pre_processing(df_prices):
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

def is_address_in_dataset(address):
    df = pd.read_csv('./markets.csv')
    row = df.loc[df['address'] == address]
    if len(row) == 0:
        return False
    else:
        return True

def get_market_name(address):
    df = pd.read_csv('./markets.csv')
    row = df.loc[df['address'] == address]
    if len(row) == 0:
        return 'Address not found'
    else:
        market_name = row['market_name'].values[0]
        asset_0 = row['asset_0'].values[0]
        asset_1 = row['asset_1'].values[0]
        return f'{market_name} ({asset_0}/{asset_1})'

def create_sankey_data(df):
    top_senders = df.groupby('sender')['sender'].count().nlargest(5).index.tolist()
    top_receivers = df.groupby('receiver')['receiver'].count().nlargest(5).index.tolist()
    
    nodes = top_senders + top_receivers
    
    node_dict = {node: i for i, node in enumerate(nodes)}
    
    links = []
    for sender in top_senders:
        sender_df = df[df['sender'] == sender]
        for receiver in top_receivers:
            count = sender_df[sender_df['receiver'] == receiver]['receiver'].count()
            if count > 0:
                links.append({'source': node_dict[sender], 'target': node_dict[receiver], 'value': count})
    
    return nodes, links

def create_sankey_graph(df):
    nodes, links = create_sankey_data(df)

    for i in range(len(nodes)):
        if is_address_in_dataset(nodes[i]):
            nodes[i] = get_market_name(nodes[i])

    fig = go.Figure(data=[go.Sankey(
        node = dict(
        pad = 15,
        thickness = 20,
        line = dict(color = "grey", width = 0.5),
        label = nodes,
        color = "white"
        ),
        link = dict(
        source = [link['source'] for link in links],
        target = [link['target'] for link in links],
        value = [link['value'] for link in links]
    ))])

    fig.update_layout(title_text="Transaction Flow", font_size=10)
    return fig

def main():
    st.set_page_config(page_title='Algorand Analytics', layout = 'wide', page_icon = './images/logo.jpg')
    st.title("Algorand Analytics")

    df_txs = pd.read_csv('./transactions_27132402.csv')
    df_prices = pd.read_csv('./responses_1676945441.csv')
    df_prices = pre_processing(df_prices)

    addresses = get_n_biggest_senders(df_txs, 5)

    fig = create_price_chart(df_prices, df_txs, addresses)
    st.plotly_chart(fig, use_container_width=True)

    fig = create_sankey_graph(df_txs)
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
