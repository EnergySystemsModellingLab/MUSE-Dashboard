import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, ALL
from dash.exceptions import PreventUpdate
import plotly.express as px
from pathlib import Path

from server.model import Model
from settings.config import TITLE, ASSETS_FOLDER, technologies, objectives


app = dash.Dash(
    title=TITLE,
    assets_folder=ASSETS_FOLDER,
    external_stylesheets=[dbc.themes.FLATLY],
    suppress_callback_exceptions=True,
)

model = Model()


navbar = dbc.Navbar(
    color="primary",
    dark=True,
    children=[
        dbc.Col(
            dbc.NavbarBrand(
                html.Img(src=app.get_asset_url("muse-logo.png"), height="30px"),
                href="/",
            )
        ),
        dbc.Col(
            dcc.Dropdown(
                id="model-dropdown",
                options=[{"label": model, "value": model} for model in model.names],
                placeholder="Select a Model",
            )
        ),
    ],
)

app.layout = html.Div(
    children=[
        navbar,
        html.Br(),
        dbc.Container(
            fluid=True,
            children=[
                dbc.Spinner(dbc.Row([dbc.Col(id="input-values")]), size="lg"),
                dbc.Spinner(dbc.Row([dbc.Col(id="capacity-graphs")]), size="lg"),
                dbc.Row([dbc.Col(id="prices-graphs")]),
            ],
        ),
    ]
)


@app.callback(
    Output("input-values", "children"),
    Input("model-dropdown", "value"),
)
def select_model(model_name):
    if model_name is None:
        raise PreventUpdate

    model.select(model_name)

    return [
        dbc.CardGroup(
            [
                dbc.Card(
                    body=True,
                    children=[
                        dbc.Label(sector.name.title(), size="lg"),
                        dbc.Label(
                            model.technodata[sector.name]["ProcessName"].iloc[-1],
                            size="sm",
                        ),
                    ]
                    + [
                        dbc.FormGroup(
                            row=True,
                            children=[
                                dbc.Label(technology, width=6),
                                dbc.Col(
                                    dbc.Input(
                                        value=model.technodata[sector.name][
                                            technology
                                        ].iloc[-1],
                                        type="number",
                                        min=min(value_range),
                                        max=max(value_range),
                                        step=0.00000001,
                                        id={
                                            "type": "input_value",
                                            "index": f"{sector.name}-{technology}",
                                        },
                                    ),
                                ),
                            ],
                        )
                        for technology, value_range in technologies.items()
                    ],
                )
                for sector in model.sectors
            ],
        ),
        dbc.CardGroup(
            [
                dbc.Card(
                    body=True,
                    children=[
                        dbc.Label(agent["AgentShare"], size="lg"),
                        dcc.Dropdown(
                            options=[
                                {"label": objective, "value": objective}
                                for objective in objectives["Objective1"]
                            ],
                            value=agent["Objective1"],
                            id={
                                "type": "agent_value",
                                "index": agent["AgentShare"],
                            },
                        ),
                    ],
                )
                for index, agent in model.agents.iterrows()
            ],
        ),
        html.Br(),
        dbc.Button("Run Model", color="primary", id="run-button"),
    ]


@app.callback(
    Output("capacity-graphs", "children"),
    Output("prices-graphs", "children"),
    Input("run-button", "n_clicks"),
    State({"type": "input_value", "index": ALL}, "value"),
    State({"type": "agent_value", "index": ALL}, "value"),
)
def make_graphs(n_clicks, input_values, agent_values):
    if n_clicks is None:
        raise PreventUpdate

    # Update input data files
    i = 0
    for sector in model.sectors:
        for technology in technologies.keys():
            model.technodata[sector.name][technology].iloc[-1] = input_values[i]
            i += 1
    for index, agent in model.agents.iterrows():
        agent["Objective1"] = agent_values[index]

    result = model.run()
    alert = None
    if result:
        alert = dbc.Alert(result, color="danger")

    fig = px.bar(
        model.capacity,
        x="year",
        y="capacity",
        color="technology",
        facet_col="sector",
    )
    fig.update_yaxes(matches=None)
    fig.update_yaxes(showticklabels=True)
    capacity_figures = [html.Br(), alert, dcc.Graph(figure=fig)]

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
