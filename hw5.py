from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 


class QuestionnaireAnalysis:
    
    def __init__(self, data_fname: Union[pathlib.Path, str])def __init__(self, data_fname):
        self.data_fname = data_fname
        self.data = self.read_data()

    def read_data(self):
        filepath = self.data_fname  
        pd.read_json(filepath)

#Q1
    def show_age_distrib(self) -> Tuple[np.ndarray, np.ndarray]:

        df = self.data
        hist, bins = np.histogram(df.age.dropna(), bins = [1,10,20,30,40,50,60,70,80,90,100])
        return (hist,bins)
#Q2
    def remove_rows_without_mail(self) -> pd.DataFrame:

        df_unfiltered = self.data
        def is_invalid_email(arg):  #check if email address is invalid
            loc_char = arg.find('@')
            if loc_char == -1 or arg[loc_char + 1] == '.':
                arg = np.nan
            
        df_filtered = df_unfiltered.email.apply(is_invalid_email, axis=1)
        df = df_filtered.dropna(subset=['email']).reset_index(drop=True)  
        return df

#Q3
    def fill_na_with_mean(self) -> Tuple[pd.DataFrame, np.ndarray]

        df = self.data
        d_ans = df[['q1','q2','q3','q4','q5']] 
        NaN_only = d_ans.isnull().any(axis=0)
        arr = NaN_only.index.values
        df = df.fillna(df.mean(subset=['q1','q2','q3','q4','q5'], axis=0))
        return tuple(df,arr)     

#Q4
    def score_subjects(self, maximal_nans_per_sub: int = 1) -> pd.DataFrame:

        df = self.data
        d_ans = df[['q1','q2','q3','q4','q5']] 
        d_ans = d_ans.fillna(d_ans.mean(axis=1),limit = maximal_nans_per_sub)
        mean_grade = d_ans.mean(axis=0).round(0).astype('UInt8')
        df['score'] = mean_grade
        return df

#Q5 BONUS
