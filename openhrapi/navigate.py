import calendar
from datetime import date

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from openhrapi.config import URL_FICHAJE, URL_PARTE, URL_CONSULTA_PARTE, URL_BASE


def get_logged_session(usuario, password):

    ua = UserAgent().random
    session = requests.session()
    session.headers['User-Agent'] = ua

    response = session.get(URL_BASE)
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
    options = soup.form.find('select').find_all('option')

    datos = [{'nombre': option.text, 'valor': option.attrs['value']}
             for option in options[:-1]]
    return datos


def new_parte(session, idproyecto, fecha: date = None, horas=8):
    response = session.get(URL_PARTE)
    soup = BeautifulSoup(response.text, features="html.parser")
    form = soup.form

    campos = form.find_all('input')
    if fecha is None:
        fecha = date.today()

    data = {"paridesqpar": "K1",
            "aReg[paridesqpar]": next(c.attrs['value'] for c in campos if c.get('name') == "aReg[paridesqpar]"),
            "aReg[paridemp]": next(c.attrs['value'] for c in campos if c.get('name') == "aReg[paridemp]"),
            "date": f"{fecha.year} - {fecha.month} - {fecha.day}",
            "aReg[parfecha][dd]": f"{fecha.day}",
            "aReg[parfecha][mm]": f"{fecha.month}",
            "aReg[parfecha][aaaa]": f"{fecha.year}",
            "aReg[pargrupotrabajo]": idproyecto,
            "aReg[conceptos][B1][parvalunidades]": horas,
            "aReg[conceptos][B1][parvalprecio]": 1.000,
            "aReg[parcomentario]": ""}
    boton = form.find(lambda x: x.get('value') == 'Grabar' and x.get('type') == 'submit')
    data[boton['name']] = boton['value']

    return session.post(form['action'], data=data).ok


def get_imputado(session, day=None):
    response = session.get(URL_CONSULTA_PARTE)
    soup = BeautifulSoup(response.text, features="html.parser")

    fecha = date.today()
    dias_mes = calendar.monthrange(fecha.year, fecha.month)[1]
    x = [is_imputado(soup.tbody.children, d) for d in range(1, dias_mes+1)]

    if day:
        return x[day.day-1]
    else:
        return dict(enumerate(x, start=1))


def is_imputado(proyectos, d):
    return any(float(list(p.children)[d + 4].text) for p in proyectos)
