import pandas as pd
from muse.mca import MCA
import muse.examples
import logging

from settings.config import MODEL_NAMES

logging.getLogger("muse").setLevel(0)


class Model:
    def __init__(self):
        self.model: MCA
        self.names = MODEL_NAMES

    def select(self, name: str = "default"):
        self.model = muse.examples.model(name)

    def run(self):
        self.model.run()

    @property
    def sectors(self):
        return [
            sector for sector in self.model.sectors if "technologies" in dir(sector)
        ]

    @property
    def capacity(self):
        return pd.read_csv("Results/MCACapacity.csv")

    @property
    def prices(self):
        return pd.read_csv("Results/MCAPrices.csv")


"""Can update the values of the data arrays directly:

mca.sectors[2].technologies.utilization_factor
mca.sectors[2].technologies["utilization_factor"].values = [[0.5],[0.5]]

UtilizationFactor, [0,1]
cap_par [0,100]
MaxCapacityAddition [0,100]
MaxCapacityGrowth [0,100]
TotalCapacityLimit [0,1000]
"""
