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


### Current Limitations:
Model is a global variable. This will need to be refactored if made into a production server. [See here](https://dash.plotly.com/sharing-data-between-callbacks)

Only the last row in `Technodata.csv` for each Sector is currently editable. Another loop comprehension and potentially a [tab component](https://dash-bootstrap-components.opensource.faculty.ai/docs/components/tabs/) will be required for more.

The dashboard itself does not have any automated tests. Only the interface with the model does.



### Program Flow:

one-click executable - pyinstaller
