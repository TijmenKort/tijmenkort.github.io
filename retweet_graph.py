
import pandas as pd
import numpy as np
import networkx as nx
import plotly.graph_objects as go

from data import import_conflict_data

CONFLICT_DF = import_conflict_data('conflict_data_ukr.csv')


def filter_to_clusters(G, clusters):
    """
    Filters the nodes of G based on attribute 'cluster'

    Return: nx.Graph()
    """

    remove_nodes_cluster = []
    for node in G.nodes():
        if G.nodes[node]['cluster'] not in set(clusters):
            remove_nodes_cluster.append(node)

    for node in remove_nodes_cluster:
        G.remove_node(node)

    return G


def component_bounds(clusters):
    """
    Create the bounds for axis of the plot, list of clusters

    Return: dict()
    """

    comps_bounds = {c: {
        'low': i,
        'high': i+0.8,
        'label': c
    } for i, c in enumerate(clusters, start=2)}

    return comps_bounds


def add_positions(G, comps_bounds):
    """
    Add positions to graph based on component_bounds
    """

    for node in G.nodes():
        G.nodes[node]['pos'] = [
            G.nodes[node]['date'],
            np.random.uniform(
                low=comps_bounds[G.nodes[node]['cluster']]['low'],
                high=comps_bounds[G.nodes[node]['cluster']]['high']
            )
        ]

    for edge in G.edges():
        G.nodes[edge[0]]['pos'] = G.nodes[edge[0]]['pos']
        G.nodes[edge[1]]['pos'] = G.nodes[edge[1]]['pos']

    return G


def conflict_scatter(conflict_df):
    """
    Set the scatter plot for conflict data

    Return: go.Scatter()
    """

    # Create nodes for conflict data
    # add nodes
    conf_node_x = []
    conf_node_y = []
    for idx in conflict_df.index:
        x, y = conflict_df.loc[idx, 'date_start'], np.random.uniform(0, 1.5)
        conf_node_x.append(x)
        conf_node_y.append(y)

    conf_node_trace = go.Scatter(
        x=conf_node_x, y=conf_node_y,
        name='Conflicts',
        mode='markers',
        customdata=conflict_df,
        hovertemplate='<i>Conflict name:</i> %{customdata[8]}<br><i>Deaths:</i> \
                       %{customdata[41]}<br><i>Date:</i> %{customdata[37]}}',
        marker=dict(size=10+(conflict_df['deaths_civilians']*5))
    )

    return conf_node_trace


def retweet_scatter(G, clusters):
    """
    Set the scatter plot for retweets with nodes and edges

    Return: go.Scatter(), go.Scatter()
    """
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#eeeeee'),
        name='Edges',
        hoverinfo='none',
        mode='lines')

    # add nodes
    node_x = {c: [] for c in clusters}
    node_y = {c: [] for c in clusters}

    for node in G.nodes():
        c = G.nodes[node]['cluster']
        x, y = G.nodes[node]['pos']
        node_x[c].append(x)
        node_y[c].append(y)

    # find cluster without nodes
    empty_clusters = [name for name, c in node_x.items() if c == []]
    # remove empty clusters
    for c in empty_clusters:
        node_x.pop(c), node_y.pop(c), clusters.remove(c)

    node_trace = []
    for c in clusters:
        node_trace.append(go.Scatter(
            x=node_x[c], y=node_y[c],
            name=c,
            mode='markers',
            hoverinfo='skip',
            hovertemplate='<i>Account:</i> No info yet',
        ))

    return edge_trace, node_trace


def build_plot(edge_trace, node_trace, conf_node_trace, comps_bounds):
    """
    Build the plot.

    Return: fig
    """
    fig = go.Figure(
        data=[edge_trace] + node_trace + [conf_node_trace],
        layout=go.Layout(
            height=800,
            colorway=['#5E0DAC', '#FF4F00', '#375CB1',
                      '#FF7400', '#FFF400', '#FF0056'],
            template='plotly_dark',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            font_family='Helvetica Neue',
            title=dict(
                text="Fake news spread through retweets",
                font=dict(family='Helvetica Neue', color='#FFFFFF', size=24),
                x=0.5,
                xanchor='center',
                y=0.92,
                yanchor='middle'
            ),

            showlegend=True,
            hovermode='closest',
            xaxis_tickformat='%d %b %Y',
            xaxis=dict(
                showgrid=True,
                gridcolor='lightpink',
                gridwidth=0.5,
                zeroline=False,
                # color='#FFFFFF',
                range=[
                    pd.to_datetime("01-01-2016"),
                    pd.to_datetime("06-06-2017")
                ],
                rangeslider_visible=True,
                type="date"
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='lightpink',
                gridwidth=0.5,
                zeroline=False,
                color='#FFFFFF',
                tickmode='array',
                tickvals=[.75] + [np.mean([
                    bounds['low'],
                    bounds['high']
                ]) for bounds in comps_bounds.values()],
                ticktext=['Conflict'] + [
                    label['label'][:30] for label in comps_bounds.values()
                ]
            )
        )
    )

    return fig


def run_retweet_graph(language, cluster=None, cluster_update=False):
    # Import retweet graph
    if language == 'all':
        # Import all retweets
        G = nx.read_gpickle('new_graphs/retweet_network.pickle')
    elif language == 'english':
        # Import only tweets with english articles
        G = nx.read_gpickle(
            'new_graphs/retweet_network_english.pickle'
        )
    elif language == 'russian':
        # Import only tweets with russian articles
        G = nx.read_gpickle(
            'new_graphs/retweet_network_russian.pickle'
        )

    if not cluster:
        cluster = sorted(list({
            G.nodes[node]['cluster'] for node in G.nodes()
        }))
        if cluster_update:
            return [{'label': f'{c}', 'value': f'{c}'} for c in cluster]
    else:
        cluster = cluster.copy()
    # Filter G to nodes with only cluster values
    G = filter_to_clusters(G, cluster)

    # Create boundries for plot, and add to graph
    comps_bounds = component_bounds(cluster)
    G = add_positions(G, comps_bounds)

    # Build scatter conflict
    conflict_df = CONFLICT_DF.copy()

    # Filter to only usable data
    conflict_df = conflict_df[
        conflict_df['date_start'] > pd.to_datetime("1-1-2016")
    ]
    conflict_df = conflict_df[
        conflict_df['date_start'] < pd.to_datetime("1-6-2017")
    ]

    conf_node_trace = conflict_scatter(conflict_df)

    # Build scatter tweets
    edge_trace, node_trace = retweet_scatter(G, cluster)

    # build total figure
    fig = build_plot(edge_trace, node_trace, conf_node_trace, comps_bounds)

    return fig
