import os
import sys
import logging

from azure.storage.blob import BlobClient

container_name = os.getenv("CONTAINER_NAME")
connection_string = os.getenv("CONNECTION_STRING")

logger = logging.getLogger('azure.storage.blob')
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)

def insert_on_blob(file_name, image):
    blob = BlobClient.from_connection_string(conn_str=connection_string, container_name=container_name, blob_name=file_name, logging_enable=True)
    blob.upload_blob(data=image)