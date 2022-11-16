import os

from azure.storage.blob.aio import BlobClient

container_name = os.getenv("CONTAINER_NAME")
connection_string = os.getenv("CONNECTION_STRING")

async def insert_on_blob(file_name, image):
    blob = BlobClient.from_connection_string(conn_str=connection_string, container_name=container_name, blob_name=file_name)
    return await blob.upload_blob(data=image)