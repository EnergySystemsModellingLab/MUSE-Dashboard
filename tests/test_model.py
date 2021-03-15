from pytest import fixture
from unittest.mock import MagicMock, patch


@fixture(autouse=True)
def change_test_dir(request, tmp_path):
    from os import chdir
    from pathlib import Path

    cwd = Path.cwd()

    chdir(tmp_path)
    yield
    chdir(cwd)


@fixture
def model():
    from server.model import Model

    return Model()


@fixture
def sectors():
    class Sector:
        def __init__(self, name, technologies=True):
            self.name = name
            if technologies:
                self.technologies = True

    return [Sector("one"), Sector("two"), Sector("three", False)]


def test_select(tmp_path, model):
    from muse.defaults import DEFAULT_OUTPUT_DIRECTORY

    model.load = MagicMock()
    model._read_data = MagicMock()
    copy_model_mock = MagicMock(return_value=tmp_path)

    with patch("muse.examples.copy_model", copy_model_mock):
        model.select("model_name")

    copy_model_mock.assert_called_with(
        name="model_name",
        path=tmp_path / "data" / "model_name",
        overwrite=True,
    )
    assert model.path == tmp_path
    assert model.output_path == tmp_path.parent / DEFAULT_OUTPUT_DIRECTORY
    model.load.assert_called()
    model._read_data.assert_called()


def test_load(tmp_path, model):
    import muse.examples

    model.output_path = tmp_path
    model.path = muse.examples.copy_model(
        name="default",
        path=tmp_path,
        overwrite=True,
    )

    mca_factory_mock = MagicMock()
    with patch("muse.mca.MCA.factory", mca_factory_mock):
        model.load()

    mca_factory_mock.assert_called()


def test_read_data(model, tmp_path, sectors):
    import pandas as pd

    model.path = tmp_path

    mock_df = pd.DataFrame({"a": [1, 2, 3], "b": [1, 2, 3], "c": [1, 2, 3]})

    with patch("pandas.read_csv", MagicMock(return_value=mock_df)), patch(
        "server.model.Model.sectors", sectors
    ):
        model._read_data()

    assert list(model.technodata.keys()) == [sector.name for sector in sectors]
    assert model.technodata["one"].equals(mock_df)
    assert model.agents.equals(mock_df)


def test_run(model):
    from muse.investments import LinearProblemError

    model._write_data = MagicMock()
    model.load = MagicMock()

    class MockModel:
        run = MagicMock(side_effect=[None, LinearProblemError("Error Message")])

    model.model = MockModel()
    result = model.run()

    model._write_data.assert_called()
    model.load.assert_called()
    model.model.run.assert_called()
    assert result is None

    result = model.run()
    assert result == "Error Message"


def test_write_data(model, tmp_path, sectors):
    import pandas as pd

    model.path = tmp_path

    mock_df = pd.DataFrame({"a": [1, 2, 3], "b": [1, 2, 3], "c": [1, 2, 3]})
    model.technodata = {}
    for sector in sectors:
        model.technodata[sector.name] = mock_df
    model.agents = mock_df

    to_csv = MagicMock(return_value=mock_df)
    with patch("pandas.DataFrame.to_csv", to_csv), patch(
        "server.model.Model.sectors", sectors
    ):
        model._write_data()

    to_csv.assert_called_with(tmp_path / "technodata" / "Agents.csv")


def test_sectors(model, sectors):
    class MockModel:
        def __init__(self, sectors):
            self.sectors = sectors

    model.model = MockModel(sectors)
    assert model.sectors == sectors[:2]


def test_result_properties(tmp_path, model):
    model.output_path = tmp_path

    result_mock = MagicMock(return_value="result")
    with patch("pandas.read_csv", result_mock):
        assert model.capacity == "result"
        result_mock.assert_called_with(tmp_path / "MCACapacity.csv")
        assert model.prices == "result"
        result_mock.assert_called_with(tmp_path / "MCAPrices.csv")
