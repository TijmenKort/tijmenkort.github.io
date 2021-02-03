import pickle
import dash_table


def run_doc_explain():
    with open('data/cluster_explain.pickle', 'rb') as f:
        doc_explain = pickle.load(f)

    # data_table = dash_table.DataTable(
    #     columns=[
    #         {"name": i, "id": i} for i in ['cluster', 'keywords',
    #                                        'average_sim', 'links']
    #     ],
    #     data=doc_explain,
    #     style_header={'backgroundColor': 'rgb(30, 30, 30)'},
    #     style_cell={
    #         'backgroundColor': 'rgb(50, 50, 50)',
    #         'color': 'white',
    #         'overflow': 'hidden',
    #         'textOverflow': 'clip',
    #         'maxWidth': 0
    #     },
    #     sort_action="native",
    #     sort_by=[{
    #         'column_id': 'cluster',
    #         'direction': 'asc',
    #     }],
    #     tooltip_data=[
    #         {
    #             column: {'value': str(value), 'type': 'markdown'}
    #             for column, value in row.items()
    #         } for row in doc_explain
    #     ],
    #     css=[{
    #         'selector': '.dash-table-tooltip',
    #         'rule': 'background-color: black; font-family: monospace;'
    #     }],
    #     tooltip_duration=None,
    #     tooltip_delay=0,
    # )

    return doc_explain
