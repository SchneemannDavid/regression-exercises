import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import os
from env import user, password, host
 
def handle_nulls(df):    
    # We keep 99.41% of the data after dropping nulls
    # round(df.dropna().shape[0] / df.shape[0], 4) returned .9941
    df = df.dropna()
    return df


def optimize_types(df):
    # Convert some columns to integers for optimization
    # fips, yearbuilt, and bedrooms, taxvaluedollarcnt, and calculatedfinishedsquarefeet can be integers
    df["fips"] = df["fips"].astype(int)
    df["yearbuilt"] = df["yearbuilt"].astype(int)
    df["bedroomcnt"] = df["bedroomcnt"].astype(int)    
    df["taxvaluedollarcnt"] = df["taxvaluedollarcnt"].astype(int)
    df["calculatedfinishedsquarefeet"] = df["calculatedfinishedsquarefeet"].astype(int)
    return df


def handle_outliers(df):
    """Manually handle outliers that do not represent properties likely for 99% of buyers and zillow visitors"""
    df = df[df.bathroomcnt <= 6]
    
    df = df[df.bedroomcnt <= 6]

    df = df[df.taxvaluedollarcnt < 1_500_000]

    return df

def clean_variables(df):
    # Drop 'taxamount' column (variable is inconsistent based on time and location of collected value, could lead to poor analysis)
    # Rename columns and 'fips' values to reflect actual location (to solidify column as categorical variable)
    df = df.drop(columns = 'taxamount')
    df = df.rename(columns = {'bedroomcnt':'bedrooms', 
                              'bathroomcnt':'bathrooms', 
                              'calculatedfinishedsquarefeet':'sq_ft', 
                              'taxvaluedollarcnt':'home_value', 
                              'yearbuilt':'year_built', 
                              'fips':'location',
                              'fullbathcnt':'full_bathrooms',
                              'garagecarcnt':'garage_spaces',
                              'lotsizesquarefeet':'lot_sq_ft'
                             })
    df.location = df.location.replace(to_replace={6037:'LA County', 6059:'Orange County', 6111:'Ventura County'})

    return df 

def feature_engineering(df):
    # Bin `year_built` by decade
    df["decade_built"] = pd.cut(x=df["year_built"], bins=[1800, 1899, 1909, 1919, 1929, 1939, 1949, 1959, 1969, 1979, 1989, 1999, 2009], labels=['1800s', '1900s', '10s', '20s', '30s', '40s', '50s', '60s', '70s', '80s', '90s', '2000s'])
    # Convert categorical variable to numeric var
    df['county_encoded'] = df.location.map({'LA County': 0, 'Orange County': 1, 'Ventura County': 2})

    df = df.dropna()

    return df

# Split for Exploration

## 
# Train, Validate, Test Split Function: for exploration
def zillow_split_explore(df):
    '''
    This function performs split on telco data, stratifying on churn.
    Returns train, validate, and test dfs.
    '''
    train_validate, test = train_test_split(df, test_size=.2,
                                        random_state=123)
    train, validate = train_test_split(train_validate, test_size=.3,
                                   random_state=123)
    return train, validate, test

### ------------------------------------------------------------------------

# Split for Modeling: X & Y dfs
def zillow_split_model(df):
    '''
    This function performs split on telco data, stratifying on churn.
    Returns both X and y train, validate, and test dfs
    '''
    
    train_validate, test = train_test_split(df, test_size=.2,
                                        random_state=123)
    train, validate = train_test_split(train_validate, test_size=.3,
                                   random_state=123)

    # Splitting train, validate, and test dfs on x and y
    x_train = train.drop(columns=['home_value'])
    x_validate = validate.drop(columns=['home_value'])
    x_test = test.drop(columns=['home_value'])

    y_train = train['home_value']
    y_validate = validate['home_value']
    y_test = test['home_value']
    
    return x_train, y_train, x_validate, y_validate, x_test, y_test


def prep_zillow(df):
    """
    Handles nulls
    optimizes or fixes data types
    handles outliers w/ manual logic
    clean variables via dropping columns and renaming features
    includes feature engineering 
    returns a clean dataframe
    Splits df into train, validate, test, and associated dfs on x and y 
    """
    df = handle_nulls(df)

    df = optimize_types(df)

    df = handle_outliers(df)

    df = clean_variables(df)

    df = feature_engineering(df)

    train, validate, test = zillow_split_explore(df)

    x_train, y_train, x_validate, y_validate, x_test, y_test = zillow_split_model(df)

    # df.to_csv("zillow.csv", index=False)

    return df, train, validate, test, x_train, y_train, x_validate, y_validate, x_test, y_test