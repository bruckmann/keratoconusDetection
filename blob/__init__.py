import os
import sys
import logging

from azure.storage.blob.aio import BlobClient

container_name = os.getenv("CONTAINER_NAME")
connection_string = os.getenv("CONNECTION_STRING")

logger = logging.getLogger('azure.storage.blob')
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)

async def insert_on_blob(file_name, image):
    blob = BlobClient.from_connection_string(conn_str=connection_string, container_name=container_name, blob_name=file_name, logging_enable=True)
    with open(image, 'rb') as data:
        return await blob.upload_blob(data=data)