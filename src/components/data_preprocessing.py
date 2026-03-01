import pandas as pd
import os

def data_preprocessing(data_dir):
    df=pd.read_pickle(data_dir)


    #keeping only male matches
    df=df[df["gender"]=="male"].copy()

    #print(df.shape)

    #keeping only matches with 20 overs

    df=df[df["overs"]==20].copy()
    #print(df.shape)

    #drop unncessary columns
    df.drop(columns=['overs','match_type','gender'],inplace=True)
    #print(df.shape)

    #extracting 1st innings data and removing 2nd innings data
    
    cleaned_rows=[]

    for _,row in df.iterrows():
        innings=row["innings"]

        first_innings=innings[0]
        key="1st innings"
        first_innings_data=first_innings[key]

        deliveries=first_innings_data["deliveries"]
        batting_team=first_innings_data["team"]
        bowling_team=[]
        teams=row["teams"]
        for t in teams:
            if t!=batting_team:
                bowling_team.append(t)
    
        cleaned_rows.append({
            "match_id":row["match_id"],
            "batting_team":batting_team,
            "bowling_team":bowling_team[0],
            "venue":row["venue"],
            "city":row["city"],
            "winner":row["winner"],
            "deliveries":deliveries
        })

    match_df=pd.DataFrame(cleaned_rows)

    #print(match_df.head())
    #print(match_df.shape)

    # Creating data frame with each row as single ball data
    # One row represents:
    # At this exact ball in this match, this batsman faced this bowler, and this many runs were scored, and a wicket did or did not fall

    ball_rows=[]

    for _,row in match_df.iterrows():
        for delivery in row['deliveries']:
            ball_no=list(delivery.keys())[0]
            ball_data=delivery[ball_no]
            runs=ball_data["runs"]
            runs_total=runs['total']

            wicket=1 if "wicket" in ball_data else 0

            batsman=ball_data['batsman']
            bowler=ball_data['bowler']

            ball_rows.append({
                "match_id":row["match_id"],
                "batting_team":row["batting_team"],
                "bowling_team":row["bowling_team"],
                "batsman":batsman,
                "bowler":bowler,
                "ball":ball_no,
                "runs":runs_total,
                "wicket":wicket,
                "city":row["city"],
                "venue":row["venue"]
            })

    ball_df=pd.DataFrame(ball_rows)
    # print(ball_df.head())
    # print(ball_df.shape)

    os.makedirs("artifacts",exist_ok=True)
    ball_df.to_pickle("artifacts/ball_df.pkl")
    