import os
import sys

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer

from networksecurity.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig
)

from networksecurity.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact
)

class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config=TrainingPipelineConfig()
        
    def start_data_ingestion(self):
        try:
            self.data_ingestion_config=DataIngestionConfig(self.training_pipeline_config)
            logging.info("Data ingestion started")
            self.data_ingestion=DataIngestion(self.data_ingestion_config)
            self.data_ingestion_artifact=self.data_ingestion.initiate_data_ingestion()
            logging.info(f"Data ingestion completed and artifact: {self.data_ingestion_artifact}")
            return self.data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e

    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact):
        try:
            self.data_validation_config=DataValidationConfig(self.training_pipeline_config)
            logging.info("Data validation started")
            self.data_validation=DataValidation(self.data_validation_config,data_ingestion_artifact)
            self.data_validation_artifact=self.data_validation.initiate_data_validation()
            logging.info(f"Data validation completed and artifact: {self.data_validation_artifact}")
            return self.data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e

    def start_data_transformation(self,data_validation_artifact:DataValidationArtifact):
        try:
            self.data_transformation_config=DataTransformationConfig(self.training_pipeline_config)
            logging.info("Data transformation started")
            self.data_transformation=DataTransformation(self.data_transformation_config,data_validation_artifact)
            self.data_transformation_artifact=self.data_transformation.initiate_data_transformation()
            logging.info(f"Data transformation completed and artifact: {self.data_transformation_artifact}")
            return self.data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e

    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact)->ModelTrainerArtifact:
        try:
            self.model_trainer_config:ModelTrainerConfig=ModelTrainerConfig(self.training_pipeline_config)
            logging.info("Model trainer started")
            self.model_trainer=ModelTrainer(self.model_trainer_config,data_transformation_artifact)
            self.model_trainer_artifact=self.model_trainer.initiate_model_trainer()
            logging.info(f"Model trainer completed and artifact: {self.model_trainer_artifact}")
            return self.model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e

    def run_pipeline(self):
        try:
            data_ingestion_artifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact=self.start_data_transformation(data_validation_artifact)
            model_trainer_artifact=self.start_model_trainer(data_transformation_artifact)
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e