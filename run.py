"""Run the Dashboard"""
from application.dash import app
from settings import config

app.run_server(debug=config.DEBUG, host=config.HOST, port=config.PORT)
