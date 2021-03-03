import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

inputs = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Label("X variable"),
                dcc.Dropdown(
                    id="x-variable",
                    options=[{"label": col, "value": col} for col in ["opt1", "opt2"]],
                    value="opt1",
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Y variable"),
                dcc.Dropdown(
                    id="y-variable",
                    options=[{"label": col, "value": col} for col in ["opt1", "opt2"]],
                    value="opt1",
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Cluster count"),
                dbc.Input(id="cluster-count", type="number", value=3),
            ]
        ),
        dbc.Button("Run Model", color="primary", block=True, id="run-button"),
    ],
    body=True,
)

app.layout = dbc.Container(
    [
        html.H1("MUSE Dashboard"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(inputs, md=4),
                dbc.Col(dcc.Graph(id="cluster-graph"), md=8),
                dbc.Alert("Hello, Bootstrap!", color="success"),
            ],
            align="center",
        ),
    ],
    className="m-5",
    fluid=True,
)


@app.callback(
    Output("cluster-graph", "figure"),
    [Input("run-button", "n_clicks")],
    [
        State("x-variable", "value"),
        State("y-variable", "value"),
        State("cluster-count", "value"),
    ],
)
def make_graph(n, x, y, n_clusters):
    # Do not run on startup
    if not n:
        return go.Figure()

    data = {
        "opt1": list(range(n_clusters)),
        "opt2": [num * num for num in range(n_clusters)],
    }

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=data[x],
            y=data[y],
            mode="markers",
            marker={"size": 8},
        )
    )

    fig.update_layout(
        title=f"{x} vs {y} Count {n_clusters}", xaxis_title=x, yaxis_title=y
    )

    return fig
