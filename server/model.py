import logging
from typing import List, Dict
from pathlib import Path
import pandas as pd
from muse.mca import MCA
import muse.examples
from muse.investments import LinearProblemError

from settings.config import MODEL_NAMES

logging.getLogger("muse").setLevel(0)


class Model:
    names: List[str] = MODEL_NAMES

    def __init__(self):
        self.model: MCA
        self.path: Path
        self.technodata: Dict[pd.DataFrame]
        self.agents: pd.DataFrame

    def select(self, name: str = "default"):
        self.path = muse.examples.copy_model(
            name=name,
            path=Path("."),
            overwrite=True,
        )
        self.load()
        self.technodata = {}
        for sec in self.sectors:
            sector = sec.name
            self.technodata[sector] = pd.read_csv(
                self.path / "technodata" / sector / "Technodata.csv"
            )
        self.agents = pd.read_csv(self.path / "technodata" / "Agents.csv")

    def load(self):
        self.model = MCA.factory(self.path / "settings.toml")

    def run(self):
        for sec in self.sectors:
            sector = sec.name
            self.technodata[sector].to_csv(
                self.path / "technodata" / sector / "Technodata.csv"
            )
        self.load()
        try:
            self.model.run()
        except LinearProblemError as err:
            return err.args[0]

    @property
    def sectors(self):
        return [
            sector for sector in self.model.sectors if "technologies" in dir(sector)
        ]

    @property
    def capacity(self):
        return pd.read_csv(Path("Results") / "MCACapacity.csv")

    @property
    def prices(self):
        return pd.read_csv(Path("Results") / "MCAPrices.csv")
