import pandas as pd
import plotly.graph_objects as go
import networkx as nx

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

def get_unique_senders(df):
    senders = df['sender'].unique()
    return list(senders)

def get_unique_recipients(df):
    recipients = df['receiver'].unique()
    return list(recipients)

def get_unique_transactions(df):
    transactions = []
    for sender, receiver in zip(df['sender'], df['receiver']):
        transactions.append([sender, receiver])
    unique_transactions = list(set(map(tuple, transactions)))
    return [list(x) for x in unique_transactions]

def create_network_graph(df):
    senders = get_unique_senders(df)
    recipients = get_unique_recipients(df)
    transactions = get_unique_transactions(df)

    G = nx.Graph()
    G.add_nodes_from(senders, bipartite=0)
    G.add_nodes_from(recipients, bipartite=1)
    G.add_edges_from(transactions)

    pos = nx.spring_layout(G)

    node_colors = ['#fff' if node in senders else '#111' for node in G.nodes()]

    edge_trace = go.Scatter(x=[], y=[], line={'width': 0.5, 'color': '#888'}, hoverinfo='text', mode='lines')
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['x'] += tuple([x0, x1, None])
        edge_trace['y'] += tuple([y0, y1, None])

    node_trace = go.Scatter(x=[], y=[], text=[], mode='markers', hoverinfo='text', marker={'size': 10, 'color': node_colors})

    for node in G.nodes():
        x, y = pos[node]
        
        node_trace['x'] = list(node_trace['x'])
        node_trace['x'] += (x,)
        node_trace['x'] = tuple(node_trace['x'])

        node_trace['y'] = list(node_trace['y'])
        node_trace['y'] += (y,)
        node_trace['y'] = tuple(node_trace['y'])

        node_trace['text'] += (node,)

        if is_address_in_dataset(node):
            exchange_descriptor =  get_market_name(node)
            node_trace['text'] += (exchange_descriptor,)
        else:
            node_trace['text'] += (node,)

    fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title='',
                    showlegend=False,
                    hovermode='closest',
                    margin={'b': 0, 'l': 0, 'r': 0, 't': 40},
                    xaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
                    yaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
                ))
    return fig

# https://towardsdatascience.com/tutorial-network-visualization-basics-with-networkx-and-plotly-and-a-little-nlp-57c9bbb55bb9