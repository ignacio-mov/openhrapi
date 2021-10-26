from datetime import date
from random import random
from time import sleep

from flask import Flask, request
from pip._internal.utils.deprecation import deprecated

from openhrapi.navigate import get_logged_session, post_fichaje, get_proyectos, is_imputado, new_parte, get_imputado
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


@app.route('/imputado', methods=['GET'])
@auth.login_required
@deprecated
def check_imputado():
    return {'imputado': get_imputado(session=auth.current_user(), day=date.today())}


@app.route('/imputaciones', methods=['GET'])
@auth.login_required
def check_imputado_mes():
    return {'imputado': get_imputado(session=auth.current_user())}


@app.route('/imputacion', methods=['POST'])
@auth.login_required
def imputa():
    ok = new_parte(session=auth.current_user(), idproyecto=request.values['proyecto'])
    return {'response': ok}
