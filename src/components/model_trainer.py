import pickle
from xgboost import XGBRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score,mean_absolute_error

def train_model(X_train,X_test,y_train,y_test):

    # model=XGBRegressor(
    #     n_estimators=100,
    #     learning_rate=0.1,
    #     max_depth=5,
    #     random_state=42
    # )
    model=XGBRegressor()
    params={
        'learning_rate':[.1,.01,.05,.001],
        'n_estimators': [8,16,32,64,128,256],
        'max_depth':[5],
        'random_state':[42]
    }
    gs=GridSearchCV(model,params,cv=3,n_jobs=-1,verbose=1)
    gs.fit(X_train,y_train)
    best_model=gs.best_estimator_
    

    y_pred=best_model.predict(X_test)

    r2=r2_score(y_test,y_pred)
    mae=mean_absolute_error(y_test,y_pred)
    print("R2:",r2)
    print("MAE:",mae)
    
    with open("artifacts/model.pkl","wb") as f:
        pickle.dump(model,f)

    return model, r2, mae