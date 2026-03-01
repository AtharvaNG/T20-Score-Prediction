import os
import pandas as pd
from yaml import safe_load
from tqdm import tqdm

def ingest_data(data_dir):

    rows=[]

    for file in tqdm(os.listdir(data_dir)):
        file_path=os.path.join(data_dir,file)

        with open (file_path,'r') as f:
            data=safe_load(f)

        info = data.get("info", {})
        outcome = info.get("outcome", {})
        toss = info.get("toss", {})

        rows.append({
            # ID
            "match_id": file.replace(".yaml", ""),

            # Match metadata
            "dates": info.get("dates"),
            "gender": info.get("gender"),
            "match_type": info.get("match_type"),
            "winner": outcome.get("winner"),
            "overs": info.get("overs"),
            "player_of_match": info.get("player_of_match"),
            "teams": info.get("teams"),
            "toss_decision": toss.get("decision"),
            "toss_winner": toss.get("winner"),
            "umpires": info.get("umpires"),
            "venue": info.get("venue"),
            "city": info.get("city"),

            # Core cricket data
            "innings": data.get("innings")
        })

    df=pd.DataFrame(rows)
    os.makedirs("artifacts",exist_ok=True)
    df.to_pickle("artifacts/raw_df.pkl")

    return df