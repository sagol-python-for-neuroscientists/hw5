import pathlib
import json
import pandas as pd
import numpy as np
class QuestionnaireAnalysis:
    """
    Reads and analyzes data generated by the questionnaire experiment.
    Should be able to accept strings and pathlib.Path objects.
    """

    def __init__(self, data_fname):
        # ...
        if type(data_fname)==str:
            self.data_fname=pathlib.Path(data_fname)
        else:
            self.data_fname=(data_fname)

    def read_data(self):
        """Reads the json data located in self.data_fname into memory, to
        the attribute self.data.
        """
        # ...
        with open(self.data_fname) as json_file:
            info=json.load(json_file)
            self.data=pd.DataFrame(info)
        return self

    def show_age_distrib(self):
        """Calculates and plots the age distribution of the participants.

        Returns
        -------
        hist : np.ndarray
        Number of people in a given bin
        bins : np.ndarray
        Bin edges
            """
        self.read_data()
        age=self.data['age']
        age[age =='nan']=np.nan
        age=age.dropna()
        counts, bins=np.histogram(age,bins=np.linspace(0,100,11))
        return (counts, bins)      






    def fill_na_with_mean(self):
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
        index = self.data['q1':'q5'].index[self.data['q1':'q5'].apply(np.isnan)]
        self.data['q1':'q5'].fillna(self.data['q1':'q5'].mean()) 
        return (self, index)

    
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
        nan_mask=self.data['q1':'q5'].isnan().sum>maximal_nans_per_sub
        self.data['score']=self.data['q1':'q5'].mean()
        self.data['score'][nan_mask]= 'NA'
        a=1
        return self


if __name__ == "__main__":
    test=QuestionnaireAnalysis('data.json')
    counts, bins=test.show_age_distrib()
    print(counts)
    print(bins)




