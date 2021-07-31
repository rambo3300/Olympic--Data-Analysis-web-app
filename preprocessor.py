
import pandas as pd

def preprocess(df, region_df):

    # filtering the summer olympics
    df = df[df['Season'] == 'Summer']
    # left joining the two dataframes based on NOC 
    df = df.merge(region_df, on = 'NOC', how = 'left')
    # dropping the duplicates
    df.drop_duplicates(inplace = True)
    # concatinate the medal columns in original df
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis = 1)

    return df 

