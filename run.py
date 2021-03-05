from application.dash import app
from settings import config

app.run_server(debug=config.debug, host=config.host, port=config.port)

# Include commandline arguments for data save location and optional different model? Or options in the dashboard?
