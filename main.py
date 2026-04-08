from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig
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
    except Exception as e:
        raise NetworkSecurityException(e,sys)