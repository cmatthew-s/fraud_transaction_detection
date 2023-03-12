import pandas as pd
import os
import numpy as np
import regex as re
import pickle
import json
import csv

from js import alert
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression 
from sklearn.metrics import accuracy_score, confusion_matrix, \
    roc_auc_score, recall_score 

class MachineLearning():

    def __init__(self):
        self.df =  pd.DataFrame({'A': []})
        self.target = pd.DataFrame({'A': []})
        self.features = pd.DataFrame({'A': []})
        self.count = 0
 
    def get_data(self):
        return self.df
    
    def check_data(self):
        if os.path.exists('./history_data.csv'):
            return True
        else:
            return False

    def random_dataframe(self, n_cols, n_rows):
        cols = ['Col-'+str(i) for i in range(1,n_cols+1)]
        idx = ['Row-'+str(i) for i in range(1,n_rows+1)]
        data = np.round(np.random.normal(size=(n_rows,n_cols)),2)
        df = pd.DataFrame(data,columns=cols,index=idx)
        return df
    
    def delete_data(self, columns):
        conditions = '^([A-Za-z0-9\s]*)$'
        if re.search(conditions, columns):
            lst_col = columns.split()
            for item in lst_col:
                if item not in self.df:
                    alert('{} not exists'.format(item))
                else:
                    self.df = self.df.drop([item], axis = 1)
        
        else:
            alert('Input must be in a space format to separate between columns')
    
    def set_target(self, value):
        self.targetValue = value.split()
        if len(self.targetValue) == 1:
            if self.targetValue[0] in self.df:
                self.target = self.df[self.targetValue[0]]
                self.features = self.df.drop(columns=[self.targetValue[0]], axis = 0)

                self.f_train, self.f_test, \
                    self.t_train, self.t_test = train_test_split(
                        self.features, 
                        self.target, 
                        test_size = 0.2, 
                        stratify = self.target,
                        random_state = 2
                    )

                alert('"{}" set as a Target!!'.format(self.targetValue[0]))
                # alert('{}'.format(self.f_train.shape[0] / self.features.shape[0] * 100))
            else:
                alert('{} not available in the dataframe'.format(value[0]))

        else:
            alert('Input must contain only one target')

    def predict(self):
        count = self.df[self.targetValue[0]].value_counts() / self.df.shape[0]
        real = count[0]
        fraud = count[1]

        # alert('{}, {}'.format(real, fraud))

        w = {0: real, 1: fraud}
        self.model = LogisticRegression(random_state = 2, class_weight = w)
        self.model.fit(self.f_train, self.t_train)

    def data_corr(self):
        return self.df.corr()

    def evaluation(self):
        f_train_predict = self.model.predict(self.f_train)
        f_test_predict = self.model.predict(self.f_test)
        
        self.train_accuracy = {
            'train_accuracy': accuracy_score(f_train_predict, self.t_train),
            'confusion_matrix': confusion_matrix(f_train_predict, self.t_train),
            'area_under_curve': roc_auc_score(f_train_predict, self.t_train),
            'recall': recall_score(f_train_predict, self.t_train),
        }

        self.test_accuracy = {
            'test': accuracy_score(f_test_predict, self.t_test),
            'confusion_matrix': confusion_matrix(f_test_predict, self.t_test),
            'area_under_curve': roc_auc_score(f_test_predict, self.t_test),
            'recall': recall_score(f_test_predict, self.t_test)
        }

        model_information = {
            'accuracy': self.test_accuracy['test'],
            'AUC': self.test_accuracy['area_under_curve']
        }

        with open('./model_accuracy.json', 'w') as f:
            json.dump(model_information, f)

        return [self.train_accuracy, self.test_accuracy]

    def safe_model(self):
        try:
            self.filename = './model.sav'
            pickle.dump(self.model, open(self.filename, 'wb'))
            alert('Model Saved! ')
        except:
            alert('Set the model first!')

    def use_model(self):
        if self.count == 0:
            self.count += 1
        else:
            self.count = 0
        
        if os.path.exists('./model.sav'):
            # NOTE: Api Fetch Data
            data = './real_time_data.csv'
            self.real_data = pd.read_csv(data)
            model = pickle.load(open('./model.sav', 'rb'))
            try:
                result = model.predict(self.real_data)
                self.real_data['Class'] = result
                self.save_csv()
                return self.real_data
            except:
                alert('Different data format! ')
        else:
            alert('Set your model first! ')

    def get_all_fraud_transaction(self, df):
        if 1 not in df['Class']:
            return pd.DataFrame({'A': []})
        else:
            return df[df.Class == 1]

    def save_csv(self):
        data = self.real_data.to_csv(path_or_buf="./predicted_result.csv", index_label=False)

