import networkx as nx
# import pandas as pd
# import numpy as np
import plotly.graph_objs as go
import pickle


def remove_singles(G):
    cluster_set = set()
    for set_ in nx.weakly_connected_components(G):
        if len(set_) > 1:
            cluster_set |= set_

    G = nx.subgraph(G, cluster_set)

    return G


def assign_node_size(degree, scaling_factor=10):
    return (degree + 1) ** 0.5 * scaling_factor


def assign_thickness(correlation, benchmark_thickness=2, scaling_factor=3):
    return benchmark_thickness * abs(correlation)**scaling_factor


def node_size(graph):
#assign node size depending on the number of connections ingoing, basically the number of documents that have maximum correlation with them
    node_size=[]
    for key, value in dict(graph.in_degree).items():
        node_size.append(assign_node_size(value))
    return node_size


def edge_width(graph):
#assign edge width based on the score of the similarity between articles
    edge_width = []
    for key, value in nx.get_edge_attributes(graph, 'score').items():
        edge_width.append(assign_thickness(value))
    return edge_width


def node_color(graph, df):
#assign node color based on the score
    node_color = []
    for i in graph.nodes():
        index = df[df['Publication (original)'] == i].index[0]
        node_color.append(df['score'][index])
    return node_color


def draw_networkx_graph(graph):
    node_sizes = node_size(graph)
    edge_widths = edge_width(graph)
    nx.draw(graph, with_labels=False, node_size=node_sizes, node_color="#e1575c",
        edge_color='#363847',  pos=nx.fruchterman_reingold_layout(graph), width=edge_widths)
    plt.show()


def get_coordinates(G):
    """Returns the positions of nodes and edges in a format for Plotly to draw the network"""
    # get list of node positions
    pos = nx.fruchterman_reingold_layout(G)

    Xnodes = [pos[n][0] for n in G.nodes()]
    Ynodes = [pos[n][1] for n in G.nodes()]

    Xedges = []
    Yedges = []
    for e in G.edges():
        # x coordinates of the nodes defining the edge e
        Xedges.extend([pos[e[0]][0], pos[e[1]][0], None])
        Yedges.extend([pos[e[0]][1], pos[e[1]][1], None])
    return Xnodes, Ynodes, Xedges, Yedges

def descriptions(dataframe, G):
    title_list = list()
    date_list = list()
    language = list()
    keywords = list()
    similarity = list()
    cluster_name = list()
    for i in G.nodes:
        index = dataframe[dataframe['Publication (original)'] == i].index[0]
        title_list.append(dataframe['Title'][index])
        date_list.append(G.nodes[i]['date'])
        language.append(dataframe['Language'][index])
        keywords.append(dataframe['Keywords'][index])
        similarity.append(dataframe['score'][index])
        cluster_name.append(G.nodes[i]['cluster'])
    title_dsp = ['Title: ' + r for r in title_list]
    date_dsp = ['Date of publication: ' + r for r in date_list]
    language_dsp = ['Language of article: ' + r for r in language]
    keywords_dsp = ['Keywords of article: ' + r for r in keywords]
    similarity_dsp = ['Similarity score with connection: ' + str(r) for r in similarity]
    cluster_name_dsp = ['Cluster: ' + r for r in cluster_name]
    return title_dsp, date_dsp, language_dsp, keywords_dsp, similarity_dsp, cluster_name_dsp


def build_graph(G, df):

    Xnodes, Ynodes, Xedges, Yedges = get_coordinates(G)
    title_dsp, date_dsp, language_dsp, keywords_dsp, similarity, cluster_name = descriptions(df, G)
    #create tooltip string by concatenating statistics
    description = [
        f"<b>{node}</b>" +
        "<br>" + cluster_name[index][:50] +
        "<br>" + title_dsp[index] +
        "<br>" + date_dsp[index] +
        "<br>" + language_dsp[index] +
        "<br>" + keywords_dsp[index] +
        "<br>" + similarity[index]
        for index, node in enumerate(G.nodes)]

    # edges
    tracer = go.Scatter(
        x=Xedges, y=Yedges,
        mode='lines',
        line= dict(color='#eeeeee', width=1),
        hoverinfo='none',
        showlegend=False
    )
    # nodes
    tracer_marker = go.Scatter(
        x=Xnodes, y=Ynodes,
        mode='markers+text',
        textposition='top center',
        marker=dict(
            size=node_size(G),
            showscale=True,
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            colorbar=dict(
                thickness=15,
                title='Similarity score',
                xanchor='left',
                titleside='right')
            ),
        hoverinfo='text',
        hovertext=description,
        showlegend=False)

    tracer_marker.marker.color = node_color(G, df)

    axis_style = dict(
        title='',
        titlefont=dict(size=20),
        showgrid=False,
        zeroline=False,
        showline=False,
        ticks='',
        showticklabels=False)


    # layout = dict(title='Visualise document similarity',
    #           width=1000,
    #           height=1000,
    #           autosize=False,
    #           showlegend=False,
    #           xaxis=axis_style,
    #           yaxis=axis_style,
    #           hovermode='closest',
    #           plot_bgcolor = '#fff')


    fig = go.Figure(
        data=[tracer, tracer_marker],
        layout=go.Layout(
            title_text='Geolocation of Tweets',
            showlegend=False,
            colorway=['#5E0DAC', '#FF4F00', '#375CB1',
                      '#FF7400', '#FFF400', '#FF0056'],
            template='plotly_dark',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            height=750,
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=False,
                showticklabels=False
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=False,
                showticklabels=False
            ),
        )
    )

    return fig


def run_similarity_graph():

    # Import dataframe similarity analyses
    with open('data/similarity_df.pickle', 'rb') as f:
        df = pickle.load(f)
    
    # Load network hidden in a list
    with open('data/similarity_network.pickle', 'rb') as f:
        G = pickle.load(f)[0]

    # Remove single node clusters
    G = remove_singles(G)

    # Build the graph 
    fig = build_graph(G, df)

    return fig