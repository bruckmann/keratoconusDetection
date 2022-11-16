import os

import psycopg2
from psycopg2 import Error

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")
database = os.getenv("POSTGRES_DB")


def db_connect():
    try:
        connection = psycopg2.connect(user=user,
                                      password=password,
                                      host=host,
                                      port=port,
                                      database=database)

        
        print("Connection stablished")
        return connection
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)


def insert(name, age, prediction_result, prediction_classification, file_name):
    try:
        connection = db_connect()

        client = connection.cursor()
        query = "INSERT INTO prediction_results (prediction_result, classification_result, patient_name, patient_age, image_id) VALUES ('{pd_result}', '{pd_class}', '{name}', '{age}', '{image_id}')".format(
            pd_result=prediction_result[0][0], pd_class=prediction_classification, name=name, age=age, image_id=file_name)
        result = client.execute(query)
        connection.commit()
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        client.close()
        connection.close()
