from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import re


class QuestionnaireAnalysis:
    
    def __init__(self, data_fname):
    # def __init__(self, data_fname: Union[pathlib.Path, str]):
        self.data_fname = data_fname
        self.data = self.read_data()

    def read_data(self):
        filepath = self.data_fname
        df = pd.DataFrame(pd.read_json(filepath))   
        return df

#Q1
    def show_age_distrib(self):
    # def show_age_distrib(self) -> Tuple[np.ndarray, np.ndarray]:

        df = self.data
        hist, bins = np.histogram(df['age'], bins = [0,10,20,30,40,50,60,70,80,90,100])
        return hist, bins
#Q2
    def remove_rows_without_mail(self) -> pd.DataFrame:

        df = self.data
        df = df[df['email'].str.contains(r'[^@]+@[^@]+\.[^@]+')]
        return df.reset_index()

#Q3
    # def fill_na_with_mean(self) -> Tuple[pd.DataFrame, np.ndarray]:
    def fill_na_with_mean(self):
        
        df = self.data
        mean_row = df[['q1','q2','q3','q4','q5']].mean(axis=1)
        arr = df.dropna(subset = ['q1','q2','q3','q4','q5']).index.values
        idxna = np.array([i for i in list(df.index.values) if i not in arr]) 
        df[['q1','q2','q3','q4','q5']] = df[['q1','q2','q3','q4','q5']].fillna(mean_row[arr])
        return df , idxna

#Q4
    def score_subjects(self, maximal_nans_per_sub: int = 1) -> pd.DataFrame:
        df = self.data
        df_temp = df[['q1','q2','q3','q4','q5']]
        mean_row = df_temp.mean(axis=1)
        arr = df_temp.dropna().index.values
        df_temp = df_temp.fillna(mean_row[arr] , limit = maximal_nans_per_sub).mean(axis = 1).apply(np.floor).astype('UInt8')
        df['score'] = df_temp
        return df
        
