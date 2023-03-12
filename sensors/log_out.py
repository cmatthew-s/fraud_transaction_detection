
import Data as data

from js import document
from pyodide import create_proxy

dt = data.Data()

def log_out(event):
    login = dt.read_all_text('./login.txt')
    Element('templates').write(login)
    setup()

def log_setup():
    element = document.getElementById('log-out')
    log = create_proxy(log_out)
    element.addEventListener('click', log)