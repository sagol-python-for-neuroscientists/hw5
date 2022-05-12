
import pathlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class QuestionnaireAnalysis:
    """
    Reads and analyzes data generated by the questionnaire experiment.
    Should be able to accept strings and pathlib.Path objects.
    """

    def __init__(self, data_fname: Union[pathlib.Path, str]):
        self.data=[]
        file_name = pathlib.Path(data_fname)
        data_fname = pathlib.Path(data_fname)
        if file_name.exists():
            self.data_fname = data_fname
        else:
            raise ValueError('Error: file not found')
        


    def read_data(self):
        """Reads the json data located in self.data_fname into memory, to
        the attribute self.data.
        """
        self.data = pd.read_json(self.data_fname)
      

    def show_age_distrib(self) -> Tuple[np.ndarray, np.ndarray]:
        """Calculates and plots the age distribution of the participants.

        Returns
        -------
        hist : np.ndarray
              Number of people in a given bin
        bins : np.ndarray
        Bin edges
        
        """
        binsa = np.arange(0, 110, 10)
        hist_values = self.data.age.values
        hist_values = pd.to_numeric(hist_values)
        plt.figure()
        (hist, bins, patches) = plt.hist(hist_values, bins = binsa)
        plt.show()

        return (hist, bins)
        
    def remove_rows_without_mail(self) -> pd.DataFrame:
        """Checks self.data for rows with invalid emails, and removes them.

        Returns
        -------
        df : pd.DataFrame
             A corrected DataFrame, i.e. the same table but with the erroneous rows removed and
             the (ordinal) index after a reset.
        """   
        valid_index = []
        for i, add_e in enumerate(self.data.email):
            correct_email = 0
            if (add_e[0] != '@') and (add_e[-1] != '@'):
                if add_e.count('@') == 1:
                    if add_e.count('@.') == 0:
                        if add_e[0] != '.' and add_e[-1] != '.':
                            if add_e.count('.') == 1:
                                correct_email = 1
            if correct_email == 1:
                valid_index.append(i)
            else:
                next
        df = self.data.loc[valid_index]
        df.index = range(len(df))
        
        return df 
    
    def fill_na_with_mean(self) -> Tuple[pd.DataFrame, np.ndarray]:
        """Finds, in the original DataFrame, the subjects that didn't answer
        all questions, and replaces that missing value with the mean of the
        other grades for that student.
        Returns
        -------
        df : pd.DataFrame
             The corrected DataFrame after insertion of the mean grade
        arr : np.ndarray
              Row indices of the students that their new grades were generated
         """
        
        index_save = []
        for ind_r, r in self.data.itterows():
            if 'nan' in r[['q1', 'q2', 'q3', 'q4', 'q5']].values:
                index_save += [ind_r]
                mean = r[['q1', 'q2', 'q3', 'q4', 'q5']].astype(float).mean()
                self.data.loc[ind_r, ['q1', 'q2', 'q3', 'q4', 'q5']] = r[['q1', 'q2', 'q3', 'q4', 'q5']].replace('nan', mean)
        df = self.data
        arr = np.array(index_save)
        return df, arr

         
        

    def score_subjects(self, maximal_nans_per_sub: int = 1) -> pd.DataFrame:
        """Calculates the average score of a subject and adds a new "score" column
    with it.

    If the subject has more than "maximal_nans_per_sub" NaN in his grades, the
    score should be NA. Otherwise, the score is simply the mean of the other grades.
    The datatype of score is UInt8, and the floating point raw numbers should be
    rounded down.

    Parameters
    ----------
    maximal_nans_per_sub : int, optional
        Number of allowed NaNs per subject before giving a NA score.

    Returns
    -------
    pd.DataFrame
        A new DF with a new column - "score".
        """
        
        self.data["score"] = ""
        
        for ind_row, row in self.data.iterrows():
            row_list = row[['q1', 'q2', 'q3', 'q4', 'q5']]
            row_list = row_list.tolist()
            if row_list.count("nan") > maximal_nans_per_sub:
                self.data.loc[ind_row, "score"] = pd.NA
            else:
                mean = row[['q1', 'q2', 'q3', 'q4', 'q5']].astype(float).mean()
                self.data.loc[index, "score"] = np.uint8(mean)

        self.data["score"] = self.data["score"].astype(pd.UInt8Dtype())
        return self.data


    def correlate_gender_age(self) -> pd.DataFrame:
        """Looks for a correlation between the gender of the subject, their age
    and the score for all five questions.

Returns
-------
pd.DataFrame
    A DataFrame with a MultiIndex containing the gender and whether the subject is above
    40 years of age, and the average score in each of the five questions.
    """
        df = self.data
        df = self.data.dropna(subset=['age'])
        mask = df['age'] > 40
        df_agen = df.drop(columns='age')
        df_agen['age'] = mask
        df_agen = df_agen.set_index(['gender', 'age'], append=True)
        new_df = df_agen[['q1', 'q2', 'q3', 'q4', 'q5']].groupby(level=['gender', 'age']).mean()
        return new_df  