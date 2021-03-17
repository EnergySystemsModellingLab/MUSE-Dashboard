# MUSE-Dashboard
A GUI for the MUSE model

Install inside a virtual environment with:
```bash
python -m pip install -r requirements.in
```

Run with:
```bash
python run.py
```

The app will be available at http://localhost:8080

### Current Limitations and Improvements required for productionising:

 - The simulation is slow to run, so there is significant time delay between running the model and the results appearing. This could be improved by caching results.

 - Some of the examples models included do not fix with the technologies and limits on their values specified in `settings/config.py`

 - Only the last row in `Technodata.csv` for each Sector is currently editable. Another loop comprehension and potentially a [tab component](https://dash-bootstrap-components.opensource.faculty.ai/docs/components/tabs/) will be required for more.

 - Model is a global variable. This will need to be refactored if made into a production server. [See here](https://dash.plotly.com/sharing-data-between-callbacks)

 - The dashboard itself does not have any tests. Only the interface with the model does. They can be run by running `pytest` in an activated virtual environment. There are no automated tests on GiHub.

 - For a one-click executable, look into pyinstaller. Note that the `app.run_server` function in `run.py` is an endless loop, so this needs to be navigated for any executable to also launch a web browser.

# Funding

This research received funding from the FCDO Climate Compatible Growth Project.
