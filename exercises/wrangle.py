import env

def wrangle_zillow():
    
    '''
    Read student_grades csv file into a pandas DataFrame,
    drop student_id column, replace whitespaces with NaN values,
    drop any rows with Null values, convert all columns to int64,
    return cleaned student grades DataFrame.
    '''
    # Acquire data from SQL.
    def get_db_url(dbname, username=env.user, hostname=env.host, passw=env.password):
        url = f'mysql+pymysql://{username}:{passw}@{hostname}/zillow'
        return url

    url = get_db_url('zillow', env.user, env.host, env.password)
    
    df = pd.read_sql('''
        SELECT  propertylandusetypeid
                bedroomcnt,
                bathroomcnt,
                calculatedfinishedsquarefeet,
                taxvaluedollarcnt,
                yearbuilt,
                taxamount,
                fips
        FROM properties_2017 as p17
        WHERE propertylandusetypeid = '261'
        ''', url)


    ## Clean data, dropping rows and converting dtypes ##

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


    return df