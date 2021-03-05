from muse.mca import MCA


class Model:
    def __init__(self, path: str = "server/data/default/settings.toml"):
        self.path = path
        self.mca = MCA.factory(self.path)

    def run(self):
        self.mca.run()

    def update(self):
        self.mca = MCA.factory(self.path)

    @property
    def sectors(self):
        return [sector for sector in self.mca.sectors if "technologies" in dir(sector)]
        # return [
        #     {"name": "residential", "technologies": [1, 2, 3]},
        #     {"name": "power", "technologies": [1, 2, 3]},
        #     {"name": "gas", "technologies": [1, 2, 3]},
        # ]


"""Can update the values of the data arrays directly:

mca.sectors[2].technologies.utilization_factor
mca.sectors[2].technologies["utilization_factor"].values = [[0.5],[0.5]]

UtilizationFactor, [0,1]
cap_par [0,100]
MaxCapacityAddition [0,100]
MaxCapacityGrowth [0,100]
TotalCapacityLimit [0,1000]
"""

data = {
    "linear": list(range(-10, 11)),
}
data["quadratic"] = [num * num for num in data["linear"]]
