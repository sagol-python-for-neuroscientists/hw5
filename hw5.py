
import pathlib
import pandas as pd
from typing import Union, Tuple
from matplotlib import pyplot as plt
import numpy as np
import json

class QuestionnaireAnalysis:
    """
    Reads and analyzes data generated by the questionnaire experiment.
    Should be able to accept strings and pathlib.Path objects.
    """

    def __init__(self, data_fname: Union[pathlib.Path, str]):
        self.data_fname = pathlib.Path(data_fname)
        if not self.data_fname.exists():
           raise ValueError("File does not exist.")

    def read_data(self):
        self.data = pd.read_json(self.data_fname)
    
    def show_age_distrib(self) -> Tuple[np.ndarray, np.ndarray]:
        
        bin_edges = list(range(0, 110, 10))
        hist, bins , extra = plt.hist(self.data["age"], bins = bin_edges)
        return (hist, bins)
    
    def remove_rows_without_mail(self) -> pd.DataFrame:
        """Checks self.data for rows with invalid emails, and removes them.
        Returns
        -------
        df : pd.DataFrame
        A corrected DataFrame, i.e. the same table but with the erroneous rows removed and
        the (ordinal) index after a reset.
        """
        new1 = self.data.copy()
        for index, row in new1.iterrows():
            if '@' in row['email'] and '.' in row['email']:
        
                if row['email'][0] == '@' :
                    new1.drop(index,inplace=True)
                if row['email'][-1] == '@':
                     new1.drop(index,inplace=True)
                if row['email'][-1] == '.':  
                     new1.drop(index,inplace=True)
                if row['email'][0] == '.':  
                     new1.drop(index,inplace=True)
            else : 
                 new1.drop(index,inplace=True)
            if '@.' in row['email'] :
             new1.drop(index,inplace=True)
        new1.reset_index(inplace=True) 
        return new1   

        
        
    
    def fill_na_with_mean(self) -> Tuple[pd.DataFrame, np.ndarray]:
  
        df_q = self.data.loc[:, 'q1':'q5']
        df_new_q = df_q.apply(lambda row: row.fillna(row.mean()), axis = 1)
        df = self.data.copy()
        df.loc[:, 'q1':'q5'] = df_new_q
        
        locat = np.where(df_q.isna().any(axis=1))[0]

        return (df, locat)

    def score_subjects(self, maximal_nans_per_sub: int = 1) -> pd.DataFrame:
        """ create a new column named 'score' """
        df_q = self.data.loc[:, 'q1':'q5']
        score = df_q.mean(axis = 1)
        NA_index = df_q.count(axis = 1) < (5- maximal_nans_per_sub)
        score[NA_index] = np.nan
        
        score = np.floor(score).astype('UInt8')
        new_df = self.data.copy()
        new_df['score'] = score

        return new_df
