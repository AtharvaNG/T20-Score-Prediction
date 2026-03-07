import pandas as pd
import os
import numpy as np

Allowed_teams=[
    'Pakistan',
 'India',
 'New Zealand',
 'South Africa',
 'West Indies',
 'Sri Lanka',
 'Bangladesh',
 'Zimbabwe',
 'England',
 'Australia'
]

def feature_engineering(input_path):
    df=pd.read_pickle(input_path)

    #FILTER ONLY SELECTED TEAMS

    df=df[df['batting_team'].isin(Allowed_teams) & df['bowling_team'].isin(Allowed_teams)].copy()

    #print(df.shape)

    #SORT THE DATA
    df=df.sort_values(
        by=['match_id','ball']
    ).reset_index(drop=True)

    #PROCESSING CITY
    #print(df.isnull().sum())
    cities=np.where(df['city'].isnull(),df['venue'].str.split().apply(lambda x:x[0]),df['city'])

    df['city']=cities
    #print(df.isnull().sum())

    df.drop(columns=['venue'],inplace =True)

    city_count=df['city'].value_counts()
    city_count=city_count[city_count>599]
    valid_cities=city_count.index.tolist()
    df=df[df['city'].isin(valid_cities)].copy()
    #print(df)

    #CALCULATE CURRENT RUNS(CUMMELATIVE RUNS)
    df['current_score']=(
        df.groupby('match_id')['runs'].cumsum()
    )

    #print(df['current_score'])


    #CALCULATE WICKETS FALLEN AND WICKETS LEFT

    df['wickets_fallen']=df.groupby('match_id')['wicket'].cumsum()
    
    df['wickets_left']=10-df['wickets_fallen']
    #print(df['wickets_left'])
    #print(df['wickets_fallen'])

    #CALCULATE BALLS LEFT

    df['ball_number']=df['ball'].astype(str).str.split(".").str[0].astype(int)*6 + df['ball'].astype(str).str.split(".").str[1].astype(int)

    df['balls_left']=120-df['ball_number']
    df['balls_left']=df['balls_left'].apply(lambda x: 0 if x<0 else x)
    #print(df)

    #CALCULATING CURRENT RUN RATE
    df['crr']=df['current_score']/(df['ball_number']/6)
    #print(df)

    #CALCULATING LAST 5 OVERS RUNS
    df['last_five_overs_runs']=df.groupby('match_id')['runs'].rolling(window=30).sum().reset_index(level=0,drop=True)

    #print(df.head(50))

    #CALCULATING FINAL SCORE

    df['final_score']=(
        df.groupby('match_id')['runs'].transform('sum')
    )
    #print(df)

    #DROPING NULL VALUES FOR LAST_FIVE_OVERS_RUNS COLUMN
    #print(df.isnull().sum())
    df.dropna(inplace=True)
    #print(df.isnull().sum())
    #print(df.shape)

    df=df[['batting_team','bowling_team','city','current_score','balls_left','wickets_left','crr','last_five_overs_runs','final_score']]

    df.reset_index(drop=True)
    df=df.sample(df.shape[0]).reset_index(drop=True)

    final_df=df.copy()
    #print(final_df)

    os.makedirs("artifacts",exist_ok=True)
    final_df.to_pickle("artifacts/final_df.pkl")
    return final_df