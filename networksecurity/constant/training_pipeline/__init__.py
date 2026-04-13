import os
import sys
import numpy as np
import pandas as pd
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


"""
Defining common constants variable for training pipeline
"""

TARGET_COLUMN="Result"
PIPELINE_NAME="network_security"
ARTIFACT_DIR="artifact"
FILE_NAME="phisingData.csv"

TRAIN_FILE_NAME="train.csv"
TEST_FILE_NAME="test.csv"

SAVED_MODEL_DIR="saved_models"
MODEL_FILE_NAME="model.pkl"

SCHEMA_FILE_PATH=os.path.join("data_schema","schema.yaml")

"""
Data ingestion related constants start with DATA_INGESTION Var name
"""

DATA_INGESTION_COLLECTION_NAME="NetworkData"
DATA_INGESTION_DATABASE_NAME="omphule77_db_user"
DATA_INGESTION_DIR_NAME="data_ingestion"
DATA_INGESTION_FEATURE_STORE_NAME="feature_store"
DATA_INGESTION_INGESTED_DIR="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO=0.2


"""
Data Validation related constants start with DATA_VALIDATION Var name
"""

DATA_VALIDATION_DIR_NAME="data_validation"
DATA_VALIDATION_VALID_DIR="validated"
DATA_VALIDATION_INVALID_DIR="invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR="drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME="report.yaml"

"""
Data Transformation related constants start with DATA_TRANSFORMATION Var name
"""

DATA_TRANSFORMATION_DIR_NAME="data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR="transformed_object"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR="transformed_data"

## KNN imputer
DATA_TRANSFORMATION_IMPUTER_PARAMS:dict={
    "missing_values":np.nan,
    "n_neighbors":3,
    "weights":"uniform"
}

PREPROCESSING_OBJECT_FILE_NAME="preprocessor.pkl"


"""
Model trainer related constants start with MODEL_TRAINER Var name
"""

MODEL_TRAINER_DIR_NAME="model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR="trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME="model.pkl"
MODEL_TRAINER_EXPECTED_SCORE:float =0.6
MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THRESHOLD:float =0.05