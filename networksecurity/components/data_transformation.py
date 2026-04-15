import os
import sys
import numpy as np
import pandas as pd
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS,TARGET_COLUMN
from networksecurity.entity.artifact_entity import DataTransformationArtifact,DataValidationArtifact
from networksecurity.entity.config_entity import DataTransformationConfig
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from networksecurity.utils.main_utils.utils import save_object,save_numpy_array_data

class DataTransformation:
    def __init__(self,data_transformation_config:DataTransformationConfig,data_validation_artifact:DataValidationArtifact):
        try:
            self.data_transformation_config=data_transformation_config
            self.data_validation_artifact=data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    @staticmethod
    def read_data(file_path:str)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def get_data_transformed_object(cls)->Pipeline:
        try:
            imputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            processor=Pipeline([
                ("imputer",imputer)
            ])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_transformation(self)->DataTransformationArtifact:
        logging.info("Enter the initiate_data_transformation method of DataTransformation class")
        try:
            logging.info("Starting data transformation")
            train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            ##Traning dataframe
            input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN])
            target_feature_train_df=train_df[TARGET_COLUMN]
            target_feature_train_df=target_feature_train_df.replace(-1,0)

            ##Testing dataframe
            input_feature_test_df=test_df.drop(columns=[TARGET_COLUMN])
            target_feature_test_df=test_df[TARGET_COLUMN]
            target_feature_test_df=target_feature_test_df.replace(-1,0)


            preprocessor=self.get_data_transformed_object()
            preprocessor_obj=preprocessor.fit(input_feature_train_df)
            transformed_input_feature_train=preprocessor_obj.transform(input_feature_train_df)
            transformed_input_feature_test=preprocessor_obj.transform(input_feature_test_df)

            train_arr=np.c_[transformed_input_feature_train,np.array(target_feature_train_df)]
            test_arr=np.c_[transformed_input_feature_test,np.array(target_feature_test_df)]

            save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_file_path,array=train_arr)
            save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_file_path,array=test_arr)
            save_object(file_path=self.data_transformation_config.transformed_object_file_path,obj=preprocessor_obj)

            save_object("final_model/preprocessor.pkl",preprocessor_obj)
            ## preparing Artifacts
            data_transformation_artifact=DataTransformationArtifact(
            transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
            transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
            transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            logging.info("Data transformation completed")
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    
