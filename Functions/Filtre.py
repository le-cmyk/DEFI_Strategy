
#---- Way to exclude some value from a dataframe

def exclude_crypto(df, list_crypto):
    if None in list_crypto:
        return df
    # filter out rows that contain any value in list_crypto
    df = df[~df.isin(list_crypto).any(axis=1)]
    return df   

#---- Way to get the unique crypto

def get_unique_crypto_values(df,exclude_list=[None],borrowed_only=0):
    if borrowed_only==1:
        union_set = set(df['Borrow'])
    elif borrowed_only==2:
       union_set = set(df['Lend'])
    else :
       # get the union of the two sets
       union_set = set(df['Borrow']) | set(df['Lend'])
    diff_set = union_set - set(exclude_list)
    # return the difference set as a list
    return [None]+list(diff_set)



