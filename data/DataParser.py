import pandas as pd
import data.ScoreCalculator as sc
import data.MongoDAO as md
import os

def get_all():
    """
        Returns a data frame with all the features for given schools
    """

    return md.get_data_frame()

def get_marks(subjects, terms = [1,2,3,4,5,6,7,8,9]):

    """
    Returns a data frame with marks for given subjects and terms for given schools

    Parameters
        ----------
        subjects : list of subjects ["History","Sinhala","English"]
        terms : list of terms from 1 to 9 [1,2]
                if not specified return marks for all the terms.
    """
    
    columns = []
        
    for subject in subjects :

        for term in terms:
            columns.append(subject + "_" + str(term));

    return get_all()[columns]

def get_demographics(features=["scholarship","f_edu","m_edu","s_num","s_edu","tution"]):
    df = get_all()
    return  df[features]

def get_lci():
    
    df = get_all()

    features = []

    for i in range(1,21):
        features.append("Lci_"+str(i))

    return  df[features]

def handle_missing_values(dataframe, how='0', is_nan = False):

    """
    Manages absent values in a data frame

    Parameters
        ----------
        dataframe : dataframe to be modified
        how : {'fill_0', 'fill_prev_avg', 'fill_this_avg', 'drop'}
    """
    if(not(is_nan)):

        if(how == '0'):
             dataframe.replace(-1, 0, inplace=True);

        elif(how == '?'):
            dataframe.replace(-1, '?', inplace=True);

    #     elif(how == 'fill_prev_avg'):
    #         # put previous average here for the subject
    #
    #     elif(how == 'fill_this_avg'):
    #         # put average mark for this term
    #
        elif(how == 'drop'):
             columns = list(dataframe.columns.values);

             for column in columns:
                dataframe = dataframe[dataframe[column] != 0]

    else :

        if (how == '0'):
            dataframe.fillna(0, inplace=True);

        elif (how == '-1'):
            dataframe.fillna(-1, inplace=True);

        elif (how == '?'):
            dataframe.fillna('?', inplace=True);
            # dataframe.astype(object).fillna('?', inplace=True);

        #     elif(how == 'fill_prev_avg'):
        #         # put previous average here for the subject
        #
        #     elif(how == 'fill_this_avg'):
        #         # put average mark for this term
        #
        elif (how == 'drop'):
            dataframe.dropna(inplace=True);

    return dataframe;

def discretize_marks(dataframe, subject):

    subjects = [subject];

    for i in range(1,9):
        subjects.append(subject+"."+str(i))

    for sub in subjects:
        grades=[]
        marks = dataframe[sub]
        for val in marks:
            if val != '?':
                if val >= 75:
                    grades.append('A')
                elif (val < 75 and val >= 65):
                    grades.append('B')
                elif (val < 65 and val >= 55):
                    grades.append('C')
                elif (val < 55 and val >=40):
                    grades.append('S')
                elif (val < 40 and val >= 0):
                    grades.append('F')
                    
        grade_series = pd.Series(grades)
        dataframe[sub] = grade_series

    return dataframe;



def generate_dataset_orange(subject, tution_score = "no", discretize = 'no'):

    features = ["Index No.", subject, subject + ".1", subject + ".2", subject + ".3", subject + ".4", subject + ".5",
                subject + ".6", subject + ".7", subject + ".8", "scholarship", "f_edu", "m_edu", "s_num", "s_edu",
                "tution", ]

    for i in range(1, 21):
        features.append("Lci_" + str(i));

    df = get_all()[features];
    df = handle_missing_values(df, '?');
    df = handle_missing_values(df, '?', is_nan=True);

    if(tution_score == "yes"):
        tution_score = sc.getTutionScore(df, subject);
        tution_score_series = pd.Series(tution_score);
        df["tution"] = tution_score_series;

    else:
        tution_category = sc.getTutionCategory(df, subject)
        tution_category_series = pd.Series(tution_category)
        df["tution"] = tution_category_series

    sibiling_score = sc.getSibilingEducationScore(df);
    sibiling_score_series = pd.Series(sibiling_score);
    df["s_edu"] = sibiling_score_series;

    if(discretize == 'yes'):
        df = discretize_marks(df,subject)
        df.to_csv('out_dec.csv')
    else:
        df.to_csv('out.csv')

def isNaN(val):
    return val != val
    
            

