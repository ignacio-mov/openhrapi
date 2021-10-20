import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from openhrapi.config import URL_FICHAJE, URL_PARTE


def get_logged_session(usuario, password):
    ua = UserAgent().random
    session = requests.session()
    session.headers['User-Agent'] = ua

    response = session.get(URL_FICHAJE)
    soup = BeautifulSoup(response.text, features="html.parser")
    form = soup.form

    campo = form.find_all('input')
    data = {c['name']: c.get('value') for c in campo if 'name' in c.attrs}

    data['FrmEntrada[usuario]'] = usuario
    data['FrmEntrada[clave]'] = password

    r = session.post(form['action'], data=data)

    if r.url.endswith('/autenticar/inicio'):
        raise ValueError('Usuario, password no válido')

    return session


def post_fichaje(session):
    response = session.get(URL_FICHAJE)

    soup = BeautifulSoup(response.text, features="html.parser")
    form = soup.form

    campos = form.find_all('input')
    data = {c['name']: c.get('value') for c in campos if c['type'] != 'submit'}
    data['aPic[localizacion][txt]'] = 'No se ha permitido el acceso a la posición del usuario.'

    boton = soup.find(lambda x: x.get('value') == 'Grabar' and x.get('type') == 'submit')
    data[boton['name']] = boton['value']

    return session.post(form['action'], data=data)


def get_proyectos(session):
    response = session.get(URL_PARTE)

    soup = BeautifulSoup(response.text, features="html.parser")
    form = soup.form

    campos = form.find_all('select')
    assert len(campos) == 1

    return [option.text for option in campos[0].children][:-1]
