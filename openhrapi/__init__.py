from flask import Flask

from openhrapi.config import LOG_LEVEL

app = Flask(__name__)

from openhrapi import main

app.logger.setLevel(LOG_LEVEL)
