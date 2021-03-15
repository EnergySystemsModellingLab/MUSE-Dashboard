from pathlib import Path

DEBUG = True
HOST = "127.0.0.1"
PORT = 8080
TITLE = "MUSE Dashboard"
MODEL_NAMES = ["default", "multiple-agents", "medium", "minimum-service", "trade"]
ASSETS_FOLDER = Path().absolute() / "application" / "static"

TECHNOLOGIES = {
    "UtilizationFactor": [0, 1],
    "cap_par": [0, 100],
    "MaxCapacityAddition": [0, 100],
    "MaxCapacityGrowth": [0, 100],
    "TotalCapacityLimit": [0, 1000],
}

OBJECTIVES = {
    "Objective1": [
        "comfort",
        "efficiency",
        "fixed_costs",
        "capital_costs",
        "emission_cost",
        "fuel_consumption_cost",
        "LCOE",  # "lifetime_levelized_cost_of_energy",
        "net_present_value",
        "equivalent_annual_cost",
    ]
}
