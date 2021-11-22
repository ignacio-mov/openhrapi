import os

URL_BASE = os.environ.get("FICHAJE")
URL_FICHAJE = f'{URL_BASE}/ZNVN1/emppicadasdirectas/inicio'
URL_PARTE = f'{URL_BASE}/E17/proemppartes/frm/paridesqpar/K1/empid/TBLCY7'
URL_CONSULTA_PARTE = f'{URL_BASE}/X12/infexportador/inicio'

LOG_LEVEL = os.environ['LOG_LEVEL']
