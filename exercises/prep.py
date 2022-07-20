from env import user, password, host
import os
import pandas as pd
 
 ## Clean data, dropping rows and converting dtypes ##

def prep_zillow():
    
    # Drop all rows with NaN values.
    df = df.dropna()

    # Converting fips, yearbuilt, and bedrooms, taxvaluedollarcnt, and calculatedfinishedsquarefeet into integers
    df["fips"] = df["fips"].astype(int)
    df["yearbuilt"] = df["yearbuilt"].astype(int)
    df["bedroomcnt"] = df["bedroomcnt"].astype(int)
    df["taxvaluedollarcnt"] = df["taxvaluedollarcnt"].astype(int)
    df["calculatedfinishedsquarefeet"] = df["calculatedfinishedsquarefeet"].astype(int)

    # Manually handle outliers that do not represent properties likely for 99% of buyers and zillow visitors 
    df = df[df.bathroomcnt <= 6]
    
    df = df[df.bedroomcnt <= 6]

    df = df[df.taxvaluedollarcnt < 2_000_000]

    return df
