import pathlib
import numpy as np
import pandas as pd
from typing import Union


class QuestionnaireAnalysis:
    """
    Reads and analyzes data generated by the questionnaire experiment.
    Should be able to accept strings and pathlib.Path objects.
    """

    def __init__(self, data_fname: Union[pathlib.Path, str]):
        self.data = []
        file_path = pathlib.Path(data_fname)
        if file_path.exists():
            self.data_fname = file_path
        else:
            raise ValueError('Error: file not found')

    def read_data(self):
        """Reads the json data located in self.data_fname into memory, to
        the attribute self.data.
        """
        self.data = pd.read_json(self.data_fname)
        
    """
        if type(self.data_fname) == 'pathlib.Path': #class 'pathlib.WindowsPath'
            with open(self.data_fname, "r") as file:
                data = json.load(file)
        elif type(self.data_fname) == 'string':
            with open(self.data_fname, "r") as file:
                data = json.loads(file)
"""
    def show_age_distrib(self) -> tuple[np.ndarray, np.ndarray]:
        """Calculates and plots the age distribution of the participants.

    Returns
        -------
    hist : np.ndarray
      Number of people in a given bin
    bins : np.ndarray
      Bin edges
    """
        hist_vals = self.data.age.values
        hist_bins = range(0, 110, 10)
        return np.histogram(hist_vals, bins = hist_bins)




p = 'data.json'
t = QuestionnaireAnalysis(p)
#print(type(t.data_fname)) #pathlib.windowspath
#print(t.data_fname) #data.json
#print(type(t)) #class
t.read_data()
#data = t.data
#print(t.data) #100 rows, 12 columns
#print(type(t.data)) #pandas data frame
#print(data.columns)
age = t.show_age_distrib()
print(age)
print(type(age))