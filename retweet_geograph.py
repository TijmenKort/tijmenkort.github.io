import networkx as nx
import plotly.graph_objects as go


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


def geo_scatters(G, clusters):
    """
    Set the scatter plot for retweets with nodes and edges

    Return: go.Scatter(), go.Scatter()
    """

    # add edges
    edge_lon = {c: [] for c in clusters}
    edge_lat = {c: [] for c in clusters}

    for start, end in G.edges():
        c = G.nodes[start]['cluster']
        edge_lat[c].append(G.nodes[start]['lat'])
        edge_lat[c].append(G.nodes[end]['lat'])
        edge_lat[c].append(None)

        edge_lon[c].append(G.nodes[start]['long'])
        edge_lon[c].append(G.nodes[end]['long'])
        edge_lon[c].append(None)

    # add nodes
    node_lon = {c: [] for c in clusters}
    node_lat = {c: [] for c in clusters}

    for node in G.nodes():
        c = G.nodes[node]['cluster']
        node_lon[c].append(G.nodes[node]['long'])
        node_lat[c].append(G.nodes[node]['lat'])

    # find cluster without nodes
    empty_clusters = [name for name, c in node_lon.items() if c == []]

    # remove empty clusters
    for c in empty_clusters:
        node_lon.pop(c), node_lat.pop(c), clusters.remove(c)

    node_trace = []
    edge_trace = []
    for c in clusters:
        node_trace.append(go.Scattergeo(
            name=c,
            lon=node_lon[c],
            lat=node_lat[c],
            hoverinfo='text',
            # text = retweets['node_user_descrip'],
            mode='markers',
            marker=dict(
                size=3,
                # color='rgb(255, 0, 0)',
                line=dict(
                    width=1,
                    # color='rgba(68, 68, 68, 0)'
                )
            )
        ))

        edge_trace.append(go.Scattergeo(
            name=c,
            locationmode='ISO-3',
            lon=edge_lon[c],
            lat=edge_lat[c],
            mode='lines',
            line=dict(width=1),  # color='red'),
            opacity=0.5
        ))

    return edge_trace, node_trace


def build_geoplot(edge_trace, node_trace):
    """
    Build the plot.

    Return: fig
    """
    fig = go.Figure(
        data=edge_trace + node_trace,
        layout=go.Layout(
            title_text='Geolocation of Tweets',
            showlegend=False,
            colorway=['#5E0DAC', '#FF4F00', '#375CB1',
                      '#FF7400', '#FFF400', '#FF0056'],
            template='plotly_dark',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            geo=go.layout.Geo(
                scope='world',
                projection_type='natural earth',
                showland=True,
                showcountries=True,
                landcolor='rgb(243, 243, 243)',
                countrycolor='rgb(204, 204, 204)',
            ),
            height=800,
        )
    )

    return fig


def run_retweet_geograph(language, cluster=None):
    # Import retweet graph
    if language == 'all':
        # Import all retweets
        G = nx.read_gpickle('new_graphs/retweet_geonetwork.pickle')
    elif language == 'english':
        # Import only tweets with english articles
        G = nx.read_gpickle(
            'new_graphs/retweet_geonetwork_english.pickle'
        )
    elif language == 'russian':
        # Import only tweets with russian articles
        G = nx.read_gpickle(
            'new_graphs/retweet_geonetwork_russian.pickle'
        )

    if not cluster:
        cluster = {G.nodes[node]['cluster'] for node in G.nodes()}
    else:
        cluster = cluster.copy()
    
    # Filter G to nodes with only cluster values
    G = filter_to_clusters(G, cluster)

    # Build scatter tweets
    edge_trace, node_trace = geo_scatters(G, cluster)

    # build total figure
    fig = build_geoplot(edge_trace, node_trace)

    return fig
