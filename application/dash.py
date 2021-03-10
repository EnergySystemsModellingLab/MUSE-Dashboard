import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
from pathlib import Path

from server.model import Model

app = dash.Dash(
    external_stylesheets=[dbc.themes.FLATLY], suppress_callback_exceptions=True
)

model = Model()

model_selection = dbc.Card(
    children=[
        dbc.FormGroup(
            [
                dbc.Label("Select Output Folder"),
                dcc.Input(
                    id="output-path",
                    type="text",
                    placeholder="Results",
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Select Model"),
                dcc.Dropdown(
                    id="model",
                    options=[{"label": model, "value": model} for model in model.names],
                    value=model.names[0],
                ),
            ]
        ),
        dbc.Button(
            "Select Model", color="primary", block=False, id="model-select-button"
        ),
    ],
    body=True,
)

app.layout = dbc.Container(
    fluid=True,
    children=[
        # navbar,
        html.H1("MUSE Dashboard"),
        html.Hr(),
        model_selection,
        dbc.Row([dbc.Col(id="input-values")]),
        dbc.Row([dbc.Col(id="capacity-graphs")]),
        dbc.Row([dbc.Col(id="prices-graphs")]),
    ],
)


@app.callback(
    Output("input-values", "children"),
    [Input("model-select-button", "n_clicks")],
    [
        State("model", "value"),
        State("output-path", "value"),
    ],
)
def select_model(n_clicks, model_name, output_path):
    if n_clicks is None:
        raise PreventUpdate

    model.select(model_name)

    return [
        dbc.CardGroup(
            [
                dbc.Card(
                    body=True,
                    children=[
                        dbc.Label(sector.name),
                        dcc.Dropdown(
                            id=sector.name,
                            options=[
                                {"label": col, "value": col}
                                for col in sector.technologies
                            ],
                            value=list(sector.technologies)[0],
                        ),
                    ],
                )
                for sector in model.sectors
            ],
        ),
        dbc.Button("Run Model", color="primary", block=True, id="run-button"),
    ]


@app.callback(
    Output("capacity-graphs", "children"),
    Output("prices-graphs", "children"),
    Input("run-button", "n_clicks"),
)
def make_graphs(n_clicks):
    if n_clicks is None:
        raise PreventUpdate

    model.run()

    fig = px.bar(
        model.capacity,
        x="year",
        y="capacity",
        color="technology",
        facet_col="sector",
    )
    fig.update_yaxes(matches=None)
    fig.update_yaxes(showticklabels=True)
    capacity_figures = [dcc.Graph(figure=fig)]

    fig = px.bar(
        model.prices,
        x="year",
        y="prices",
        color="commodity",
        facet_col="commodity",
    )
    fig.update_yaxes(matches=None)
    fig.update_yaxes(showticklabels=True)
    prices_figures = [dcc.Graph(figure=fig)]

    return capacity_figures, prices_figures
