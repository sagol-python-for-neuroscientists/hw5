from pathlib import Path
import pathlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from typing import Union , Tuple


class QuestionnaireAnalysis:
    
    def __init__(self, data_fname: Union[pathlib.Path, str]):
        self.data_fname = pathlib.Path(data_fname).resolve()
        if not self.data_fname.exists():
            raise ValueError("File doesn't exist")


    def read_data(self):
        self.data = pd.read_json(self.data_fname)   

#Q1
    def show_age_distrib(self) -> Tuple[np.ndarray, np.ndarray]:

        df = self.data
        hist, bins = np.histogram(df['age'], bins = [0,10,20,30,40,50,60,70,80,90,100])
        return (hist, bins)

#Q2
    def remove_rows_without_mail(self) -> pd.DataFrame:

        df = self.data
        df = df[df['email'].str.contains(r'[^@]+@[^@]+\.[^@]+')]
        return df.reset_index()

#Q3
    def fill_na_with_mean(self) -> Tuple[pd.DataFrame, np.ndarray]:
        
        df = self.data
        mean_row = df.loc[:,['q1','q2','q3','q4','q5']].mean(axis=1)
        idxval = df.dropna(subset = ['q1','q2','q3','q4','q5']).index.values
        arr = np.array([i for i in list(df.index.values) if i not in idxval]) 
        df.loc[:,['q1','q2','q3','q4','q5']] =  df.loc[:,['q1','q2','q3','q4','q5']].fillna(mean_row[arr],axis=0)
        return (df , arr)


#Q4
    def score_subjects(self, maximal_nans_per_sub: int = 1) -> pd.DataFrame:
        df = self.data
        df_temp = df.loc[:,['q1','q2','q3','q4','q5']]
        mean_row = df_temp.mean(axis=1)
        for i , m in enumerate(mean_row):
            df_temp.loc[i,:] = df_temp.loc[i,:].fillna(m, limit = 1)
        df['score'] = df_temp.mean(skipna=False, axis=1).apply(np.floor).astype('UInt8')
        return df
    
#Q5
    def correlate_gender_age(self) -> pd.DataFrame:
        df = self.data
        df_filtered = df.loc[:,['gender','age','q1','q2','q3','q4','q5']]
        df_filtered['age'] = df_filtered['age'].dropna() > 40 
        grouped = df_filtered.groupby(['gender','age'] , as_index=True).mean()
        return grouped

