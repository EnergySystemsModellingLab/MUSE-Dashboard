import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

from server.model import data, Model

app = dash.Dash(external_stylesheets=[dbc.themes.SKETCHY])

model = Model()

# path = Path("server") / "data" / "default"
# list(path.glob("technodata/gas/*"))

# Initially load only the input widgets to upload input data and select output path

inputs = dbc.Card(  # Move this to a callback
    [
        dbc.FormGroup(
            [
                dbc.Label(sector.name),
                dcc.Dropdown(
                    id=sector.name,
                    options=[
                        {"label": col, "value": col} for col in sector.technologies
                    ],
                    value=list(sector.technologies)[0],
                ),
            ]
        )
        for sector in model.sectors
    ],
    body=True,
)

toy_inputs = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Label("X variable"),
                dcc.Dropdown(
                    id="x-variable",
                    options=[{"label": col, "value": col} for col in data.keys()],
                    value=list(data.keys())[0],
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Y variable"),
                dcc.Dropdown(
                    id="y-variable",
                    options=[{"label": col, "value": col} for col in data.keys()],
                    value=list(data.keys())[1],
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Number of Points"),
                dbc.Input(
                    id="point-count",
                    type="number",
                    value=11,
                    min=1,
                    max=len(data["linear"]),
                ),
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
        dbc.Col([inputs], align="left", md=4),
        dbc.Row(
            [
                dbc.Col(toy_inputs, md=4),
                dbc.Col(
                    dcc.Graph(id="cluster-graph"),
                    md=6,
                ),
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
        State("point-count", "value"),
    ],
)
def make_graph(n, x, y, n_points):
    # Do not run on startup
    if not n:
        return go.Figure()

    midpoint = int(len(data[x]) // 2)
    minmax = int(n_points // 2)
    left = midpoint - minmax
    right = midpoint + minmax + n_points % 2

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=data[x][left:right],
            y=data[y][left:right],
            mode="markers",
            marker={"size": 8},
        )
    )

    fig.update_layout(
        title=f"{x} vs {y} Count {n_points}", xaxis_title=x, yaxis_title=y
    )

    return fig
