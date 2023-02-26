import pandas as pd

def preprocess(df,region_df):

    df = df[df['Season'] == 'Summer']

    df = df.merge(region_df, on='NOC', how='left')

    df.drop_duplicates(inplace=True)

    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)

    a = df[df['Year'] == 1906].index

    index = []
    for i in range(len(a)):
        if a[i] not in index:
            index.append(a[i])

    df.drop(index, inplace=True)

    return df

def winter_process(df,region_df):

    df = df[df['Season'] == 'Winter']

    df = df.merge(region_df, on='NOC', how='left')

    df.drop_duplicates(inplace=True)

    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)

    # a = df[df['Year'] == 1906].index
    #
    # index = []
    # for i in range(len(a)):
    #     if a[i] not in index:
    #         index.append(a[i])
    #
    # df.drop(index, inplace=True)

    return df