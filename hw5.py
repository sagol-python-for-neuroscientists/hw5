import numpy as np
import pathlib
from typing import Union, Tuple
import pandas as pd

class QuestionnaireAnalysis:
    
    def __init__(self, data_fname: Union[pathlib.Path, str]):
        data_fname = pathlib.Path(data_fname)
        if not data_fname.exists():
            raise ValueError('file not found: {}'.format(data_fname))
        self.data_fname = data_fname

    def read_data(self):
        self.data = pd.read_json(self.data_fname)
        return self.data

    def show_age_distrib(self) -> Tuple[np.ndarray, np.ndarray]:
        bins = np.arange(0, 101, 10)
        distribution = pd.cut(self.data['age'], bins, right = False)
        hist = np.array(pd.value_counts(distribution).sort_index())
        return hist, bins

    def remove_rows_without_mail(self) -> pd.DataFrame:
        drop_list = []
        for index, mail in enumerate(self.data['email']):
            str_place = mail.find('@')
            if mail.count('@') != 1:
                drop_list.append(index)
            elif mail[str_place + 1] == '.':
                drop_list.append(index)
            elif mail.count('.') == 0:
                drop_list.append(index)    
              
        correct_data = self.data.drop(drop_list)
        return correct_data.reset_index()

    def fill_na_with_mean(self) -> Tuple[pd.DataFrame, np.ndarray]:
        q_columns = self.data.loc[: , "q1":"q5"]
        changed_index = pd.isnull(q_columns).any(1).to_numpy().nonzero()[0]
        correct_columns = q_columns.apply(lambda row: row.fillna(row.mean()), axis=1)
        self.data.loc[: , "q1":"q5"] = correct_columns
        return self.data, changed_index   

    def score_subjects(self, maximal_nans_per_sub: int = 1) -> pd.DataFrame:
        q_columns = self.data.loc[: , "q1":"q5"]
        number_of_nan = pd.isnull(q_columns).sum(axis=1)  
        nan_index = number_of_nan[number_of_nan > maximal_nans_per_sub].index.values.astype(int)
        score = pd.Series(q_columns.mean(axis=1).apply(np.floor).astype("UInt8"))
        score[nan_index] = np.nan
        score_df = self.data
        score_df['score'] = score 
        return score_df 

    def correlate_gender_age(self) -> pd.DataFrame:
        by_groups = self.data[['age', 'gender', 'q1', 'q2', 'q3', 'q4', 'q5']]
        replace_nan = by_groups['age'].replace(np.nan, 50)
        age_condition = (replace_nan >= 40)
        by_groups['age'] = age_condition
        final = by_groups.groupby(['gender', 'age']).mean()
        return final