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

        client = connection.cursor()
        print("Connection stablished")
        return client
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)


def insert(name, age, prediction_result, prediction_classification):
    try:
        client = db_connect()

        query = "INSERT INTO prediction_results (prediction_result, classification_result, patient_name, patient_age) VALUES ('{pd_result}', '{pd_class}', '{name}', '{age}')".format(
            pd_result=prediction_result[0][0], pd_class=prediction_classification, name=name, age=age)
        result = client.execute(query)
        print(result)
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        client.close()
