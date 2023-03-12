import pandas as pd
import numpy as np
import Data

class Specialist:
    
    def __init__(self):
       self.dt = Data.Data() 
    
    def sample_data(self, input, path):
        self.df = pd.read_csv(path) # real data
        d = self.df.sample(n=input)
        
        return(d)

    def manual_prediction(self, data):
        data['Results'] = 0
        return data
  
    def update(self, rows):
        self.dt.html_to_csv(rows)
