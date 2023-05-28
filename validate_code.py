from hw5 import *

# Create an instance of QuestionnaireAnalysis
analysis = QuestionnaireAnalysis('data.json')

# Read the data from the file
data = analysis.read_data()

# Access the loaded data
data = analysis.data

# call all the methods to make sure they work
analysis.show_age_distrib()
analysis.fill_na_with_mean()
analysis.remove_rows_without_mail()


# call the fill_na_with_mean method to get a corrected DataFrame and the indices of the corrected rows
df, corrected_indices = analysis.fill_na_with_mean()
print(df)
print(corrected_indices)






# use the show_age_distrib method to plot the age distribution
# return the number pf participants in a given bin, and the bin edges
# hist, bins = analysis.show_age_distrib()
# # print nicely how many participants are in each bin, in a loop
# for i in range(len(hist)):
#     print(f'{hist[i]} participants are between {bins[i]} and {bins[i+1]} years old')