import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

import numpy as np
import pandas as pd
import dill
import pickle
import os
import sys

from sklearn.metrics import f1_score
from sklearn.model_selection import GridSearchCV

def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path,"r") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def write_yaml_file(file_path:str,content:object ,replace:bool=True)->None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"w") as file:
            yaml.dump(content,file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def save_numpy_array_data(file_path:str,array:np.array):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e

def save_object(file_path:str,obj:object)->None:
    try:
        logging.info(f"Enter the save object method of utils")
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            pickle.dump(obj,file_obj)
        logging.info(f"Exit the save object method of utils")
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e

def load_object(file_path:str)->object:
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist")
        with open(file_path,"rb") as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e

def load_numpy_array_data(file_path:str)->np.array:
    try:
        with open(file_path,"rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e

def evaluate_model(x_train,y_train,x_test,y_test,models,params):
    try:
        report={}

        for model_name, model in models.items():
            
            param = params[model_name]
            gs = GridSearchCV(model,param,cv=3)
            gs.fit(x_train,y_train)
            
            
            model.set_params(**gs.best_params_)
            model.fit(x_train,y_train)

            y_train_pred=model.predict(x_train)
            y_test_pred=model.predict(x_test)

            train_model_score=f1_score(y_train,y_train_pred)
            test_model_score=f1_score(y_test,y_test_pred)

            report[model_name]=test_model_score

        return report


            
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e
