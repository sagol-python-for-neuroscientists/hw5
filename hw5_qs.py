from typing import Union
import numpy as np
import pathlib
import pandas as pd
import matplotlib.pyplot as plt




class QuestionnaireAnalysis:
    """
    Reads and analyzes data generated by the questionnaire experiment.
    Should be able to accept strings and pathlib.Path objects.
    """

    def __init__(self, data_fname: Union[pathlib.Path, str]):
        self.data_fname = pathlib.Path(pathlib.Path.cwd().joinpath(pathlib.Path(data_fname)))
        # ...
        

    def read_data(self):
        """Reads the json data located in self.data_fname into memory, to the attribute self.dat """
        self.dat = pd.read_json(self.data_fname)

    
    def show_age_distrib(self) -> tuple[np.ndarray, np.ndarray]:
        """
        Calculates and plots the age distribution of the participants. 
        The bins for the histogram should be [0, 10), [10, 20), [20, 30), ..., [90, 100]

   Returns
   -------
   hist : np.ndarray
     Number of people in a given bin
   bins : np.ndarray
     Bin edges
        
        
        
        """
        self.dat = self.dat.dropna(subset=["age"])
        bins = np.arange(0, 101, 10)
        counts, edges, plot = plt.hist(self.dat['age'], bins)
        plt.show()
        return counts, edges



        






        



