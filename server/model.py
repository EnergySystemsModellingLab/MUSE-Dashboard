from typing import Dict, Union
from pathlib import Path
import pandas as pd
from muse.mca import MCA
import muse.examples
from muse.investments import LinearProblemError
from muse.readers.toml import read_settings
from muse.defaults import DEFAULT_OUTPUT_DIRECTORY


class Model:
    """Interface between MUSE and the dashboard."""

    def __init__(self):
        self.model: MCA
        self.path: Path
        self.output_path: Path
        self.technodata: Dict[pd.DataFrame]
        self.agents: pd.DataFrame

    def select(self, name: str = "default"):
        """Select an example model from MUSE.

        Args:
            name (str): The model name. Defaults to "default".
        """
        self.path = muse.examples.copy_model(
            name=name,
            path=Path.cwd() / "data" / name,
            overwrite=True,
        )
        self.output_path = self.path.parent / DEFAULT_OUTPUT_DIRECTORY
        self.load()
        self._read_data()

    def _read_data(self):
        """Read the technodata and agents data so the dashboard can edit/show them."""
        self.technodata = {}
        for sec in self.sectors:
            sector = sec.name
            self.technodata[sector] = pd.read_csv(
                self.path / "technodata" / sector / "Technodata.csv"
            )
        self.agents = pd.read_csv(self.path / "technodata" / "Agents.csv")

    def load(self):
        """Load the chosen example model. Change output path to be unique per model."""
        settings = read_settings(self.path / "settings.toml")

        def prepend_path(outputs):
            for index, output in enumerate(outputs):
                relative_path = Path(output["filename"]).relative_to(Path.cwd())
                outputs[index]["filename"] = self.path.parent / relative_path

        prepend_path(settings.outputs)
        for sector in settings.sectors:
            if type(sector) == list:
                continue
            if "outputs" not in dir(sector):
                continue
            prepend_path(sector.outputs)

        self.model = MCA.factory(settings)

    def run(self) -> Union[None, str]:
        """Save changes to input data and then run the model.

        Returns and error message string if there is a LinearProblemError in the
        simulation.

        Returns:
            Optional[str]: LinearProblemError message.
        """
        self._write_data()
        self.load()
        try:
            self.model.run()
        except LinearProblemError as err:
            return err.args[0]
        return None

    def _write_data(self):
        """Save changes to the technodata and agents data so the model can use them."""
        for sec in self.sectors:
            sector = sec.name
            self.technodata[sector].to_csv(
                self.path / "technodata" / sector / "Technodata.csv"
            )
        self.agents.to_csv(self.path / "technodata" / "Agents.csv")

    @property
    def sectors(self) -> list:
        """A list of Sectors with editable technodata in the chosen model.

        Returns:
            sectors (list): List of Sectors.
        """
        return [
            sector for sector in self.model.sectors if "technologies" in dir(sector)
        ]

    @property
    def capacity(self) -> pd.DataFrame:
        """Reads the capacity results.

        Returns:
            pd.DataFrame: Capacity for the MCA.
        """
        return pd.read_csv(self.output_path / "MCACapacity.csv")

    @property
    def prices(self) -> pd.DataFrame:
        """Reads the prices results.

        Returns:
            pd.DataFrame: Prices for the MCA.
        """
        return pd.read_csv(self.output_path / "MCAPrices.csv")
