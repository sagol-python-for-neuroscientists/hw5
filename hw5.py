# -*- coding: utf-8 -*-
"""
Created on Tue May  3 18:21:57 2022

@author: Avigaill
"""

import pathlib
from typing import Union
import pandas as pd
import numpy as np

class QuestionnaireAnalysis:
    
    def __init__(self, data_fname: Union[pathlib.Path, str]):
        try:
            self.data_fname = pathlib.Path(data_fname).resolve()
        except TypeError:
            print('Data type not valid')
            raise
        if not self.data_fname.is_file():
            raise ValueError('File not valid')
    
    def read_data(self):
        self.data = pd.read_json(self.data_fname)
        return self.data

    def show_age_distrib(self):
        #define bin size
        bins = []
        for x in range(0, 110, 10):
            bins.append(x) 
        #arrays of distribution and bins
        hist = np.histogram(self.data['age'], bins=bins)
        
        return hist
    
    def remove_rows_without_mail(self):
        #defined conditions
        cond1 = (self.data['email'].str.count('@')==1) & ~(self.data['email'].str.startswith('@')) & ~(self.data['email'].str.endswith('@')) 
        cond2 = (self.data['email'].str.count('\\.') > 0) & ~(self.data['email'].str.startswith('\\.')) & ~(self.data['email'].str.endswith('\\.')) 
        cond3 = ~(self.data['email'].str.contains('@\\.'))
        
        #filter df based on conditions and reset index
        valid_df = self.data[cond1 & cond2 & cond3]
        valid_df.reset_index(drop=True, inplace=True)
        
        return valid_df
    
    def fill_na_with_mean(self):
        #find index of nan values
        index_nan_q1 = list(self.data['q1'].index[self.data['q1'].apply(np.isnan)])
        index_nan_q2 = list(self.data['q2'].index[self.data['q2'].apply(np.isnan)])
        index_nan_q3 = list(self.data['q3'].index[self.data['q3'].apply(np.isnan)])
        index_nan_q4 = list(self.data['q4'].index[self.data['q4'].apply(np.isnan)])
        index_nan_q5 = list(self.data['q5'].index[self.data['q5'].apply(np.isnan)])
        
        #concat to one list and transform to numpy array
        all_replaced_ind = index_nan_q1 + index_nan_q2 + index_nan_q3 + index_nan_q4 + index_nan_q5
        arr = np.array(all_replaced_ind)
        arr = np.sort(arr)
        arr = np.unique(arr)
        
        #replace nan with average 
        self.data['q1'] = self.data['q1'].fillna(self.data['q1'].mean())
        self.data['q2'] = self.data['q2'].fillna(self.data['q2'].mean())
        self.data['q3'] = self.data['q3'].fillna(self.data['q3'].mean())
        self.data['q4'] = self.data['q4'].fillna(self.data['q4'].mean())
        self.data['q5'] = self.data['q5'].fillna(self.data['q5'].mean())
        
        return (self.data, arr) 
    
    def score_subjects(self, maximal_nans_per_sub: int = 1):
        #create new score column with nan values
        self.data['score'] = np.nan
        #define columns to calculate score by
        cols = self.data.loc[: , "q1":"q5"]
        #if there is less than X nan values, calculate mean score
        self.data.loc[self.data.loc[: , "q1":"q5"].isnull().sum(axis=1) <= maximal_nans_per_sub, 'score'] = cols.mean(axis=1)
        #round down score and change data type
        self.data['score'] = self.data['score'].apply(np.floor).astype('UInt8')
        
        return self.data
    
    def correlate_gender_age(self):
        #remove nan values
        new_df = self.data[self.data['age'].notna()]
        #change age column to indicate whether age is above or under 40 
        new_df['age'] = np.where(new_df['age'] > 40, True, False)
        #set gender and age column as index
        new_df = new_df.set_index(['gender', 'age'])
        #groupby gender and age and calculate mean score for each questionnaire
        mean_score_by_gen_age = new_df.groupby(['gender', 'age'])['q1', 'q2', 'q3', 'q4', 'q5'].mean()
        
        return mean_score_by_gen_age
