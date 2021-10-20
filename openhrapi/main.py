from random import random
from time import sleep

from flask import Flask

from openhrapi.navigate import get_logged_session, post_fichaje, get_proyectos
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    try:
        s = get_logged_session(usuario=username, password=password)
    except ValueError as ex:
        app.logger.info(ex)
        app.logger.debug(username, password)
        return False

    sleep(random() * 5 + 5)
    return s


@app.route('/ficha', methods=['POST'])
@auth.login_required
def fichar():
    post_fichaje(session=auth.current_user())
    return {}


@app.route('/proyectos', methods=['GET'])
@auth.login_required
def proyectos():
    return {'proyectos': get_proyectos(session=auth.current_user())}
