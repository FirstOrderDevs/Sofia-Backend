import pandas as pd
import os
from classes.student import Student


def get_all(schools=["sirisaman", "southland"]):
    """
        Returns a data frame with all the features for given schools
    """
    dirname = os.path.dirname(__file__)

    files = [];

    for school in schools:
        files.append(school + "_full.csv");

    path = os.path.join(dirname, "../Data/");

    dataframes = [];

    for file in files:
        df = pd.read_csv(path + file);

        dataframes.append(df);

    merged_df = dataframes[0];

    for dataframe in dataframes[1:]:
        merged_df = merged_df.append(dataframe);

    return merged_df;

class Data :
    students = []
    teachers = []


