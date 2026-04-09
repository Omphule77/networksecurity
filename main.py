from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig,DataValidationConfig,DataTransformationConfig
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
import sys
if __name__=="__main__":
    try:
       trainingpipelineconfig=TrainingPipelineConfig()
       dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
       dataingestion=DataIngestion(dataingestionconfig)
       logging.info("Starting data ingestion")
       dataingestionartifact=dataingestion.initiate_data_ingestion()
       logging.info("Data ingestion completed")
       print(dataingestionartifact)
       data_validation_config=DataValidationConfig(trainingpipelineconfig)
       data_validation=DataValidation(data_validation_config,dataingestionartifact)
       logging.info("Starting data validation")
       data_validation_artifact=data_validation.initiate_data_validation()
       logging.info("Data validation completed")
       print(data_validation_artifact)
       data_transformation_config=DataTransformationConfig(trainingpipelineconfig)
       data_transformation=DataTransformation(data_transformation_config,data_validation_artifact)
       logging.info("Starting data transformation")
       data_transformation_artifact=data_transformation.initiate_data_transformation()
       logging.info("Data transformation completed")
       print(data_transformation_artifact)
    except Exception as e:
        raise NetworkSecurityException(e,sys)