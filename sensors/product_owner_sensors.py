
import Data as data
import pandas as pd
import os
import MLDev as mldev

from js import alert, console

dt = data.Data()
ml = mldev.MachineLearning()

def owner_setup():
    if os.path.exists('./predicted_result.csv'):
        df = pd.read_csv('./predicted_result.csv')
        Element('prediction-result-all').write('Loading..')
        display_data('prediction-result-all', df)

        fraud_data = ml.get_all_fraud_transaction(df)
        if fraud_data.empty:
            Element('fraud-transaction').write('No Fraud Transaction Detected')
        else:
            Element('fraud-transaction').write('Loading..')
            display_data('fraud-transaction', fraud_data)


