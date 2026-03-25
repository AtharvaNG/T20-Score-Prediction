import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.compose import ColumnTransformer
import pickle

categorical_features=["batting_team","bowling_team","city"]
numerical_features=["current_score","balls_left","wickets_left","crr","last_five_overs_runs"]

def data_transormation(input_path):
    df=pd.read_pickle(input_path)
    X=df.drop(columns=["final_score"])
    Y=df["final_score"]

    X_train,X_test,y_train,y_test = train_test_split(X,Y,test_size=0.2,random_state=42)

    preprocessor=ColumnTransformer(
        transformers=[
            ("cat",OneHotEncoder(handle_unknown="ignore"),categorical_features),
            ("num",StandardScaler(),numerical_features)
        ]
    )

    X_train=preprocessor.fit_transform(X_train)
    X_test=preprocessor.transform(X_test)

    with open("artifacts/preprocessor.pkl","wb") as f:
        pickle.dump(preprocessor,f)

    return X_train,X_test,y_test,y_train

