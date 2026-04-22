import os,sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

class S3sync:
    def sync_folder_to_s3(self,folder,aws_bucket_url):
        try:
            command=f"python -m awscli s3 sync {folder} {aws_bucket_url}"
            os.system(command)
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e

    def sync_folder_from_s3(self,folder,aws_bucket_url):
        try:
            command=f"python -m awscli s3 sync {aws_bucket_url} {folder}"
            os.system(command)
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e