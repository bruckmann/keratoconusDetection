import os

from azure.storage.blob.aio import BlobClient

import utils

container_name = os.getenv("CONTAINER_NAME")
connection_string = os.getenv("CONNECTION_STRING")

async def insert_on_blob(person_name: str, image):
    name_to_save = utils.format_file_name(person_name)
    blob = BlobClient.from_connection_string(conn_str=connection_string, container_name=container_name, blob_name=name_to_save)
    await blob.upload_blob(data=image)
    return name_to_save