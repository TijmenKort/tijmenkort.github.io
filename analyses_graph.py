import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def build_graph(frequencies_df, clusters):
    """
    Build the graph

    Return fig
    """

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    if clusters:
        for c in clusters:
            fig.add_trace(
                go.Scatter(
                    x=frequencies_df['date'],
                    y=frequencies_df[c],
                    name=f"Tweets {c}"
                ),
                secondary_y=False,
            )

    fig.add_trace(
            go.Scatter(
                x=frequencies_df['date'],
                y=frequencies_df['sum'],
                name="Tweets sum"
            ),
            secondary_y=False,
        )

    fig.add_trace(
        go.Scatter(
            x=frequencies_df['date'],
            y=frequencies_df['conflicts'],
            name="Conflicts Ukrain"
        ),
        secondary_y=True,
    )

    # Add styling to analysis graph visualisation
    fig.update_layout(
        height=800,
        title_text="Frequency conflicts vs tweets",
        font_family="Helvetica Neue",
        colorway=['#5E0DAC', '#FF4F00', '#375CB1',
                  '#FF7400', '#FFF400', '#FF0056'],
        template='plotly_dark',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        xaxis=dict(
                showgrid=True,
                gridcolor='lightpink',
                # gridwidth=0.5,
                range=[
                    pd.to_datetime("01-01-2016"),
                    pd.to_datetime("31-12-2016")
                ],
                rangeslider_visible=True,
                type="date"
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='lightgrey')
    )

    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Tweets</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Conflicts</b>", secondary_y=True, gridcolor ='pink')

    # fig.update_xaxes(
    #     rangeslider_visible=True,
    # )

    return fig


def run_analyses_graph(clusters):

    frequencies_df = pd.read_csv('new_graphs/tweet-conflict_frequencies.csv')
    fig = build_graph(frequencies_df, clusters)

    return fig
