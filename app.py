from pandas.core.dtypes.common import classes
import os
import sys

import certifi
ca=certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url=os.getenv("MONGODB_URI_KEY")
print(mongo_db_url)
import pymongo
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

from fastapi import FastAPI,Request,UploadFile,File
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run as app_run
from fastapi.responses import Response,RedirectResponse
import pandas as pd

from networksecurity.utils.main_utils.utils import load_object

client=pymongo.MongoClient(mongo_db_url,tlsCAFile=ca)

from networksecurity.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME,DATA_INGESTION_DATABASE_NAME

database=client[DATA_INGESTION_DATABASE_NAME]
collection=database[DATA_INGESTION_COLLECTION_NAME]

from fastapi.templating import Jinja2Templates
templates=Jinja2Templates(directory="./templates")

app=FastAPI()
origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/",tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        training_pipeline=TrainingPipeline()
        training_pipeline.run_pipeline()
        return Response("Training pipeline completed successfully")
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e

@app.post("/predict")
async def predict(request:Request,file:UploadFile=File(...)):
    try:
        df=pd.read_csv(file.file)
        preprocessor=load_object("final_model/preprocessor.pkl")
        final_model=load_object("final_model/model.pkl")

        networkmodel=NetworkModel(preprocessor=preprocessor,model=final_model)
        print(df.iloc[0])
        y_pred=networkmodel.predict(df)
        print(y_pred)
        df['predicted_column']=y_pred
        print(df['predicted_column'])
        df.to_csv("prediction_outputs/output.csv")
        table_html=df.to_html(classes="table table-striped")
        return templates.TemplateResponse(
            request=request, name="table.html", context={"table": table_html}
        )
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e

if __name__=="__main__":
    app_run(app,host="localhost",port=8000)
        
