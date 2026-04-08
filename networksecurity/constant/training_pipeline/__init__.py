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