import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from retweet_graph import run_retweet_graph
from retweet_geograph import run_retweet_geograph
from analyses_graph import run_analyses_graph
from analyses_scores import run_analyses_scores
from similarity_graph import run_similarity_graph
from doc_explain import run_doc_explain

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__)
# , external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[html.Div(
    className='row',
    children=[
        html.Div(
            # className='two columns div-user-controls',
            className='two columns',
            children=[
                html.H2('THE SPREAD OF FAKE NEWS'),
                html.P('Visualising the distribution of \
                        fake news articles through twitter'),
                # Language selector
                # html.P('Select a language:'),
                html.Div(
                    className='div-user-controls div-for-dropdown',
                    children=[
                        dcc.Dropdown(
                            id='language-selector',
                            options=[
                                {'label': u'All languages', 'value': 'all'},
                                {'label': 'English', 'value': 'english'},
                                {'label': 'Russian', 'value': 'russian'}
                            ],
                            className='countryselector',
                            value='all',
                            clearable=False,
                        ),
                    ],
                ),
                # Cluster selector
                html.Div(
                    className='div-user-controls div-for-checklist',
                    children=[
                        # html.P('Select the clusters:'),
                        dcc.Checklist(
                            id='cluster-selector',
                            className='selector-checklist',

                        )]
                    )]
        ),
        html.Div(
            className='eight columns div-for-charts bg-grey',
            children=[
                html.Div(
                    className="row",
                    children=[
                        dcc.Tabs(
                            id="tabs-with-classes",
                            value='tab-2',
                            parent_className='custom-tabs',
                            className='custom-tabs-container',
                            children=[
                                dcc.Tab(
                                    label='Histogram',
                                    value='tab-1',
                                    id='histo_tab',
                                    className='custom-tab',
                                    selected_className='custom-tab--selected',
                                    children=[
                                        dcc.Graph(id='histogram'),
                                    ]
                                ),
                                dcc.Tab(
                                    label='Analysis Graph',
                                    value='tab-2',
                                    id='analysis_tab',
                                    className='custom-tab',
                                    selected_className='custom-tab--selected',
                                    children=[
                                        dcc.Graph(id='analysis-graph'),
                                    ]
                                ),
                                dcc.Tab(
                                    label='Document Similarities',
                                    value='tab-3',
                                    id='sim_tab',
                                    className='custom-tab',
                                    selected_className='custom-tab--selected',
                                    children=[
                                        dcc.Graph(id='similarity-graph'),
                                    ]
                                ),
                                dcc.Tab(
                                    label='Geo Graph',
                                    value='tab-4',
                                    id='geo_tab',
                                    className='custom-tab',
                                    selected_className='custom-tab--selected',
                                    children=[
                                        dcc.Graph(id='geo-graph'),
                                    ],
                                )
                            ],
                            colors={
                                "border": "#1E1E1E",
                                "primary": '#fd7e14',
                                "background": '#1E1E1E',
                            },
                            # style={'color': '#1E1E1E'}
                        ),
                    ]
                ),
                html.Div(
                    className="row",
                    children=[
                        dash_table.DataTable(
                            id='hist-data-table',
                            columns=[
                                {"name": i, "id": i} for i in [
                                    'cluster', 'keywords',
                                    'average_sim', 'links'
                                ]
                            ],
                            style_header={
                                'backgroundColor': 'rgb(30, 30, 30)'
                            },
                            style_cell={
                                'backgroundColor': 'rgb(50, 50, 50)',
                                'color': 'white',
                                'overflow': 'hidden',
                                'textOverflow': 'clip',
                                'maxWidth': 0
                            },
                            sort_action="native",
                            sort_by=[{
                                'column_id': 'cluster',
                                'direction': 'asc',
                            }],
                            css=[{
                                'selector': '.dash-table-tooltip',
                                'rule': 'background-color: black; font-family: monospace;'
                            }],
                            tooltip_duration=None,
                            tooltip_delay=0,
                        )
                    ]
                )
            ]),
        html.Div(
            className="two columns",
            children=[
                html.H3("Results"),
                dash_table.DataTable(
                    id='pearson_r_table',
                    # className='table',
                    columns=[
                        {"name": i, "id": i} for i in ['Cluster', 'Pearson R']
                    ],
                    style_header={'backgroundColor': 'rgb(30, 30, 30)'},
                    style_cell={
                        'font-family': 'Helvetica Neue',
                        'backgroundColor': 'rgb(50, 50, 50)',
                        'color': 'white'
                    },
                    sort_action="native",
                    sort_by=[{
                        'column_id': 'Pearson R',
                        'direction': 'asc',
                    }],
                ),
            ],

        ),
    ]
)])


@app.callback(
    # Set initial cluster-selector options
    Output('cluster-selector', 'options'),
    # Set initial cluster-selector values
    Output('cluster-selector', 'value'),
    # Updates from run_retweet
    Output('similarity-graph', 'figure'),

    # Gives value to run_retweet
    Input('language-selector', 'value'),
)
def update_graph_initial(language):
    cluster_options = run_retweet_graph(language, cluster_update=True)
    cluster_values = [c['label'] for c in cluster_options][:3]
    similarities = run_similarity_graph()

    return cluster_options, cluster_values, similarities


@app.callback(
    # Updates from run_retweet
    Output('histogram', 'figure'),
    # Update geo graph
    Output('geo-graph', 'figure'),
    # Updates from run_analyses
    Output('analysis-graph', 'figure'),
    # Updates pearson r scores
    Output('pearson_r_table', 'data'),


    # Gives value to run_retweet
    Input('language-selector', 'value'),
    # Updates the selected clusters
    Input('cluster-selector', 'value')
)
def update_graph_values(language, clusters):
    run_retweet = run_retweet_graph(language, clusters)
    run_geo = run_retweet_geograph(language, clusters)
    run_analyses = run_analyses_graph(clusters)
    r_scores = run_analyses_scores(clusters)

    return run_retweet, run_geo, run_analyses, r_scores


@app.callback(
    Output('hist-data-table', 'data'),
    Output('hist-data-table', 'tooltip_data'),

    # Gives value to run_retweet
    Input('language-selector', 'value'),
)
def update_data_table(language):
    data_table = run_doc_explain()
    tooltip = [{
        column: {'value': str(value), 'type': 'markdown'}
        for column, value in row.items()
    } for row in data_table]

    return data_table, tooltip


if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
