# import dash
# import dash_core_components as dcc
# import dash_bootstrap_components as dbc
# import dash_html_components as html
# from dash.dependencies import Input, Output
# from datetime import datetime
# import pandas as pd

# from retweet_graph import run_retweet_graph
# from analyses_graph import run_analyses_graph

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# tabs = dash.Dash(external_stylesheets=external_stylesheets)
# colors = {
#     'background': '#111111',
#     'text': '#7FDBFF'
# }

# tabs.layout = html.Div(children=[html.Div(
#     className='row',
#     children=[
#     dcc.Tabs(
#         id="tabs-with-classes",
#         value='tab-2',
#         parent_className='custom-tabs',
#         className='custom-tabs-container',
#         children=[
#             dcc.Tab(
#                 label='Tab one',
#                 value='tab-1',
#                 className='custom-tab',
#                 selected_className='custom-tab--selected'
#             ),
#             dcc.Tab(
#                 label='Tab two',
#                 value='tab-2',
#                 className='custom-tab',
#                 selected_className='custom-tab--selected'
#             ),
#             dcc.Tab(
#                 label='Tab three, multiline',
#                 value='tab-3', className='custom-tab',
#                 selected_className='custom-tab--selected'
#             ),
#         ]),
#         ],
#     html.Div(id='tabs-content-classes')
#     )
# ])


# @tabs.callback(Output('tabs-content-classes', 'children'),
#               Input('tabs-with-classes', 'value'))
# def render_content(tab):
#     if tab == 'tab-1':
#         return html.Div([
#             html.H3('Tab content 1')
#         ])
#     elif tab == 'tab-2':
#         return html.Div([
#             html.H3('Tab content 2')
#         ])
#     elif tab == 'tab-3':
#         return html.Div([
#             html.H3('Tab content 3')
#         ])


# if __name__ == '__main__':
#     tabs.run_server(debug=True,port=8051)
