import pandas as pd
import plotly.graph_objects as go

def is_address_in_dataset(address):
    df = pd.read_csv('./dashboard/markets.csv')
    row = df.loc[df['address'] == address]
    if len(row) == 0:
        return False
    else:
        return True

def get_market_name(address):
    df = pd.read_csv('./dashboard/markets.csv')
    row = df.loc[df['address'] == address]
    if len(row) == 0:
        return 'Address not found'
    else:
        market_name = row['market_name'].values[0]
        asset_0 = row['asset_0'].values[0]
        asset_1 = row['asset_1'].values[0]
        return f'{market_name} ({asset_0}/{asset_1})'

def create_sankey_data(df, n):
    top_senders = df.groupby('sender')['sender'].count().nlargest(n).index.tolist()
    top_receivers = df.groupby('receiver')['receiver'].count().nlargest(n).index.tolist()
    
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

def create_sankey_graph(df, n):
    nodes, links = create_sankey_data(df, n)

    for i in range(len(nodes)):
        if is_address_in_dataset(nodes[i]):
            nodes[i] = get_market_name(nodes[i])

    fig = go.Figure(
        data=[
            go.Sankey(
                node = dict(
                    pad = 15,
                    thickness = 10,
                    line = dict(color = "gray", width = 0.5),
                    label = nodes,
                    color=["blue", "green", "yellow", "red"]
                ),
                link = dict(
                    source = [link['source'] for link in links],
                    target = [link['target'] for link in links],
                    value = [link['value'] for link in links],
                    
                )
            )
        ]
    )

    fig.update_layout(title_text="Transaction Flow", font_size=10)
    return fig