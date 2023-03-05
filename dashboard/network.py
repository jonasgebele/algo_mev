import pandas as pd
import plotly.graph_objects as go
import networkx as nx


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

    node_colors = ['#1f77b4' if node in senders else '#ff7f0e' for node in G.nodes()]

    edge_trace = go.Scatter(x=[], y=[], line={'width': 0.5, 'color': '#888'}, hoverinfo='none', mode='lines')
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


def main():
    pass

if __name__ == "__main__":
    main()