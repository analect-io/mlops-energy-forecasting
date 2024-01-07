import json
import logging
from pathlib import Path
from typing import Optional, Union
import joblib

import pandas as pd
import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv
import s3fs
from batch_prediction_pipeline import settings


def get_logger(name: str) -> logging.Logger:
    """
    Template for getting a logger.

    Args:
        name: Name of the logger.

    Returns: Logger.
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(name)

    return logger


def load_model(model_path: Union[str, Path]):
    """
    Template for loading a model.

    Args:
        model_path: Path to the model.

    Returns: Loaded model.
    """

    return joblib.load(model_path)


def save_json(data: dict, file_name: str, save_dir: str = settings.OUTPUT_DIR):
    """
    Save a dictionary as a JSON file.

    Args:
        data: data to save.
        file_name: Name of the JSON file.
        save_dir: Directory to save the JSON file.

    Returns: None
    """

    data_path = Path(save_dir) / file_name
    with open(data_path, "w") as f:
        json.dump(data, f)


def load_json(file_name: str, save_dir: str = settings.OUTPUT_DIR) -> dict:
    """
    Load a JSON file.

    Args:
        file_name: Name of the JSON file.
        save_dir: Directory of the JSON file.

    Returns: Dictionary with the data.
    """

    data_path = Path(save_dir) / file_name
    with open(data_path, "r") as f:
        return json.load(f)


def write_df_to_s3(bucket_name, file_name, df):
    """Write a dataframe to an S3 bucket as a parquet file.

    Args:
        bucket_name (S3 bucket): The bucket to write to.
        file_name (str): The name of the blob to write to. Must be a parquet file.
        df (pd.DataFrame): The dataframe to write to S3.
    """
    load_dotenv()
    ACCESS_KEY = os.getenv('ACCESS_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')

    s3 = s3fs.S3FileSystem(key=ACCESS_KEY, secret=SECRET_KEY)
    with s3.open(f's3://{bucket_name}/{file_name}', 'wb') as f:
        df.to_parquet(f)

def read_parquet_from_s3(bucket_name, file_name):
    """Reads a file from a bucket and returns a dataframe.

    Args:
        bucket_name: The bucket to read from.
        file_name: The name of the file to read.

    Returns:
        A dataframe containing the data from the file.
    """

    load_dotenv()
    ACCESS_KEY = os.getenv('ACCESS_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')
    s3 = s3fs.S3FileSystem(key=ACCESS_KEY, secret=SECRET_KEY)
    with s3.open(f's3://{bucket_name}/{file_name}', 'rb') as f:
        df = pd.read_parquet(f)
        return df
