import os

from azure.storage.blob import BlobClient

import utils

container_name = os.getenv("CONTAINER_NAME")
connection_string = os.getenv("CONNECTION_STRING")

def insert_on_blob(person_name, image):
    file_name_on_blob = utils.format_file_name(person_name)
    blob = BlobClient.from_connection_string(conn_str=connection_string, container_name=container_name, blob_name=file_name_on_blob)
    blob.upload_blob(data=image)
    return file_name_on_blob
