import os
import sys

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.entity.artifact_entity import ModelTrainerArtifact,DataTransformationArtifact

from networksecurity.utils.ml_utils.metric.classification_matric import get_classification_score
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import load_numpy_array_data,save_object,load_object,evaluate_model

from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier
)

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import f1_score


class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig, data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e

    def train_model(self,x_train,y_train,x_test,y_test):
        try:
            model={
                "Logistic Regression":LogisticRegression(),
                "Random Forest Classifier":RandomForestClassifier(),
                "Gradient Boosting Classifier":GradientBoostingClassifier(),
                "Decision Tree Classifier":DecisionTreeClassifier(),
                "KNeighbors Classifier":KNeighborsClassifier(),
                "AdaBoost Classifier":AdaBoostClassifier()
            }

            params={
                "Decision Tree Classifier": {
                    'criterion':['gini', 'entropy'],
                },
                "Random Forest Classifier":{
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Gradient Boosting Classifier":{
                    'learning_rate':[.1,.01,.05,.001],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Logistic Regression":{},
                "KNeighbors Classifier":{
                    'n_neighbors':[5,7,9,11],
                },
                "AdaBoost Classifier":{
                    'learning_rate':[.1,.01,0.5,.001],
                    'n_estimators': [8,16,32,64,128,256]
                }
                
            }
            model_report:dict=evaluate_model(x_train,y_train,x_test,y_test,model,params)
            logging.info("Model report generated successfully")

            ## To get  best model from report
            best_model_score=max(sorted(model_report.values()))

            ## To get best model name
            best_model_name=list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            ## To get best model
            best_model=model[best_model_name]
            y_train_predict=best_model.predict(x_train)
            classification_train_matric=get_classification_score(y_train,y_train_predict)

            ## To get test metrics
            y_test_predict=best_model.predict(x_test)
            classification_test_matric=get_classification_score(y_test,y_test_predict)

            preprocessor=load_object(self.data_transformation_artifact.transformed_object_file_path)
            model_dir_path=os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path,exist_ok=True)
            
            network_model=NetworkModel(preprocessor=preprocessor,model=best_model)
            save_object(self.model_trainer_config.trained_model_file_path,network_model)

            ## Model trainer Artifact
            model_trainer_artifact=ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                train_metric_artifact=classification_train_matric,
                test_metric_artifact=classification_test_matric
            )
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact


            

            
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e

    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            train_file_path=self.data_transformation_artifact.transformed_train_file_path
            test_file_path=self.data_transformation_artifact.transformed_test_file_path

            ## loading training array and testing array
            train_arr=load_numpy_array_data(train_file_path)
            test_arr=load_numpy_array_data(test_file_path)

            ## splitting training array and testing array into x and y
            x_train,y_train,x_test,y_test=(
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )

            ## train model
            model_trainer_artifact=self.train_model(x_train,y_train,x_test,y_test)
            return model_trainer_artifact

            
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e