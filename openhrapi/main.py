from datetime import date
from random import random
from time import sleep

from flask import request
from flask_caching import Cache
from flask_httpauth import HTTPBasicAuth

from openhrapi import app
from openhrapi.navigate import get_logged_session, post_fichaje, get_proyectos, new_parte, get_imputado

cache = Cache(app, config={'CACHE_TYPE': 'flask_caching.contrib.uwsgicache.UWSGICache',
                           'CACHE_UWSGI_NAME': 'openhr_cache'})

auth = HTTPBasicAuth()


@auth.verify_password
@cache.memoize(120)
def verify_password(username, password):
    app.logger.debug(f'autenticando "{username}"')
    try:
        s = get_logged_session(usuario=username, password=password)
    except ValueError as ex:
        app.logger.info(ex)
        app.logger.debug(f'{username}:{password}')
        return False

    sleep(random() * 5 + 5)
    app.logger.debug(f'Session: {s.cookies}')
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
def check_imputado():
    return {'imputado': get_imputado(session=auth.current_user(), day=date.today())}


@app.route('/imputaciones', methods=['GET'])
@auth.login_required
def check_imputado_mes():
    return {'imputado': get_imputado(session=auth.current_user())}


@app.route('/imputacion', methods=['POST'])
@auth.login_required
def imputa():
    dia = date.today()
    if param_dia := request.values['dia']:
        dia = dia.replace(day=int(param_dia))
    ok = new_parte(session=auth.current_user(), idproyecto=request.values['proyecto'], fecha=dia)
    return {'response': ok}
