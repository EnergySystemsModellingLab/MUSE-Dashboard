import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, ALL
from dash.exceptions import PreventUpdate
import plotly.express as px

from server.model import Model
from settings.config import TITLE, ASSETS_FOLDER, MODEL_NAMES, TECHNOLOGIES, OBJECTIVES


app = dash.Dash(
    title=TITLE,
    assets_folder=ASSETS_FOLDER,
    external_stylesheets=[dbc.themes.FLATLY],
    suppress_callback_exceptions=True,
)

model = Model()  # Global variable: should be reimplemented for production server


# Navbar across the top of the page. Includes logo and dropdown to select model
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
                options=[{"label": model, "value": model} for model in MODEL_NAMES],
                placeholder="Select a Model",
            )
        ),
    ],
)

# Master layout for the whole dashboard. Includes the navbar and a container that holds
# loading spinners and space for the inputs and graphs.
app.layout = html.Div(
    children=[
        navbar,
        html.Br(),
        dbc.Container(
            fluid=True,
            children=[
                dbc.Spinner(dbc.Row([dbc.Col(id="input-values")]), size="lg"),
                dbc.Spinner(dbc.Row([dbc.Col(id="graphs")]), size="lg"),
            ],
        ),
    ]
)


@app.callback(
    Output("input-values", "children"),
    Input("model-dropdown", "value"),
)
def select_model(model_name) -> list:
    """Populate the input data fields depending on the selected model.

    First triggered when a model is selected from the dropdown in the navbar.
    Loads an example MUSE model and populates the cards to edit input values.
    Does not run on startup.

    Args:
        model_name (str): The name of the selected model. From the dropdown.

    Returns:
        children (list): The children of the `input-values` Column. Contains:
            - A CardGroup for input values (technologies)
            - A CardGroup for agent values (objectives)
            - A Button to run the model using values within the CardGroup fields.
    """
    # Do not run on startup
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
                        for technology, value_range in TECHNOLOGIES.items()
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
                                for objective in OBJECTIVES["Objective1"]
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
    Output("graphs", "children"),
    Input("run-button", "n_clicks"),
    State({"type": "input_value", "index": ALL}, "value"),
    State({"type": "agent_value", "index": ALL}, "value"),
)
def make_graphs(n_clicks, input_values, agent_values) -> list:
    """Run the MUSE simulation and generate plots.

    First triggered when the Run Model button is clicked
    Loads an example MUSE model and populates the cards to edit input values.
    Does not run on startup.

    Args:
        n_clicks (int): Number of times the run button is clicked.
            A change in this value triggers this callback
        input_values (list): A list of the input values.
            The order is determined by looping over sectors and technologies.
        agent_values (list): A list of the agent (objective) values.
            The order is determined by looping over agents.

    Returns:
        children (list): The children of the `graphs` column. Contains:
            - An alert for when the simulation cannot be completed
            - A Plotly Figure with the capacity graphs
            - A Plotly Figure with the prices graphs
    """
    if n_clicks is None:
        raise PreventUpdate

    # Update input data files
    i = 0
    for sector in model.sectors:
        for technology in TECHNOLOGIES.keys():
            model.technodata[sector.name][technology].iloc[-1] = input_values[i]
            i += 1
    for index, agent in model.agents.iterrows():
        model.agents["Objective1"].iloc[index] = agent_values[index]

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
    children = [html.Br(), alert, dcc.Graph(figure=fig)]

    fig = px.bar(
        model.prices,
        x="year",
        y="prices",
        color="commodity",
        facet_col="commodity",
    )
    fig.update_yaxes(matches=None)
    fig.update_yaxes(showticklabels=True)
    children.append(dcc.Graph(figure=fig))

    return children
