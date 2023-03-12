
import TrainnedSpecialist as specialist
import os

from js import document, alert
from pyodide import create_proxy

ts = specialist.Specialist()

def manual_prediction(data):
    data = ts.manual_prediction(data)
    display_data('update-area', data, n = data.shape[0])
    edit_column(data)

def edit_column(data):
    table = document.querySelectorAll('.dataframe')
    table = table[1]
    for i in range(0, data.shape[0]):
        cell = table.rows[i].cells[data.shape[1]]
        cell.setAttribute('contenteditable', 'true')


def sample(event):
    path = './predicted_result.csv'
    if os.path.exists(path):
        value = Element('total-sampled-data').value
        if value != '':
            try:
                value = int(value)
                if int(value) > 0:
                    sample_data = ts.sample_data(int(value), path)
                    display_data('show-sample-data', sample_data)
                    manual_prediction(sample_data)
            except:
                alert('Input must be an interger')
        else:
            alert('Please fill in the total number of sampled data')
    else:
        alert('Machine Learning Developer hasn\'t set any model')

def update(event):
    table = document.querySelectorAll('.dataframe')
    if table != '':
        table = table[1]
        rows = table.getElementsByTagName('tr')
        ts.update(rows)
    else:
        alert('Take random sample of your data')

def specialist_setup():
    sample_element  = document.getElementById('start-sample')
    sample_data = create_proxy(sample)
    sample_element.addEventListener('click', sample_data)

    update_element = document.getElementById('update-sampled-renew-data')
    update_func = create_proxy(update)
    update_element.addEventListener('click', update_func)



