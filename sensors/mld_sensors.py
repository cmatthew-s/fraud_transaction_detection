
import MLDev as MLDev
import seaborn as sns
import matplotlib.pyplot as plt
import Data as data
import pandas as pd
import js
import asyncio
import os

from js import alert, document, FileReader
from pyodide import create_proxy
from io import StringIO

mld = MLDev.MachineLearning()
dt = data.Data()

def display_corr():
    cor = mld.data_corr()
    fig, ax = plt.subplots(1, 1, sharex=True, sharey=True, figsize=(13, 10))
    sns.heatmap(cor, square = True, cbar = True, fmt='.1f', annot=True, annot_kws = {'size': 8},cmap = 'Blues')
    pyscript.write('correlation', fig)

def display_data(element, df, n = 20):
    try:
        html_table = df.head(n).to_html(classes='pd-table')
        pyscript.write(element, html_table)
    except:
        pyscript.write(element, 'Could not access data')

def delete_data(event):
    value = Element('deleted-columns').value
    if value != '':
        mld.delete_data(value)
        pyscript.write('show-data', 'loading...')
        display_data('show-data', mld.get_data())
        display_corr()

def set_target(*args, **kwargs):
    value = Element('target-data').value
    mld.set_target(value)

def write_accuracy(text):
    id = [
        'train-accuracy-value', 'train-matrix', 
        'train-auc', 'train-recall', 'val-accuracy-value',
        'val-matrix', 'val-auc', 'val-recall'
    ]
    j = 0
    for i in range(0, len(id)):
        if i >= len(text):
            j = 0
        
        Element(id[i]).write(text[j])
        j += 1


def predict(*args, **kwargs):
    if mld.target.empty == False:
        write_accuracy(['Evaluating...'])
        
        mld.predict()
        alert('Finish Generating Model')
        accuracy = mld.evaluation()
        
        train_accuracy = list(accuracy[0].values())
        test_accuracy = list(accuracy[1].values())
        accuracy_item = train_accuracy + test_accuracy
        write_accuracy(accuracy_item)
    else:
        alert('Please set a Target First')

def safe_model(*args, **kwargs):
    mld.safe_model()
    data = dt.load_json('./model_accuracy.json')
    Element('use-model-accuracy').write(data['accuracy'])
    Element('use-model-auc').write(data['AUC'])

def start_prediction(*args, **kwargs):
    count = mld.count
    predict = document.getElementById('start-prediction')
    Element('prediction-result').write('loading...')

    if count == 0:
        predict.value = 'Stop Prediction'
    else:
        predict.value = 'Start Prediction'

    result = mld.use_model()
    print(result)
    display_data('prediction-result', result)

def show_file(event):
    data = event.target.result
    df = pd.read_csv(StringIO(data))
    mld.df = df
    display_data('show-data', df)
    display_corr()

async def submit_file(event):
    file = document.getElementById('submitted-data-csv').files
    if len(file) > 0:
        Element('show-data').write('Loading...')
        for f in file:
            reader = FileReader.new()
            onload_event = create_proxy(show_file)
            alert('Done!')
        
            reader.onload = onload_event
            reader.readAsText(f)
    else:
        alert('Please upload a File!')

    return

def show_data_sample_result():
    if os.path.exists('./manual_result.csv'):
        data = pd.read_csv('./manual_result.csv')
        display_data('sample-machine-learning-data', data)
    else:
        alert('not exists')

def ml_setup():
    # show_data_sample_result()
    data = document.getElementById('submit-file')
    submit_data = create_proxy(submit_file)
    data.addEventListener('click', submit_data)

    data_del = document.getElementById('deleted-col')
    del_data = create_proxy(delete_data)
    data_del.addEventListener('click', del_data)

    target = document.getElementById('target')
    target_set = create_proxy(set_target)
    target.addEventListener('click', target_set)

    element_predict = document.getElementById('predict')
    start = create_proxy(predict)
    element_predict.addEventListener('click', start)

    safe = document.getElementById('safe')
    model = create_proxy(safe_model)
    safe.addEventListener('click', model)

    real_predict = document.getElementById('start-prediction')
    real_start = create_proxy(start_prediction)
    real_predict.addEventListener('click', real_start)