import pickle
import pandas as pd

class PredictPipeline:

    def __init__(self):
        
        with open ("artifacts/preprocessor.pkl","rb") as f:
            self.preprocessor=pickle.load(f)

        with open("artifacts/model.pkl","rb") as f:
            self.model=pickle.load(f)

    
    def predict(self,input_data):

        #convert the data to data frame
        df=pd.DataFrame([input_data])

        #apply same transformation
        transformation=self.preprocessor.transform(df)

        #predict
        predict=self.model.predict(transformation)

        return int(round(predict[0]))