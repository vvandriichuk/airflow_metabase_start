from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from utils.db import get_db_url
import datatable as dt
import dataset
import time
import pandas as pd
from os import listdir
from os.path import isfile, join

DAG_ID = os.path.basename(__file__).replace('.pyc', '').replace('.py', '')

WORKFLOW_DEFAULT_ARGS = {
    'owner': 'vandriichuk',
    'start_date': datetime(2021, 7, 21),
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': 300,
    'email_on_retry': False
}

CONN_ID = 'postgres-metabase'


#############################################################################
# Extract / Transform
#############################################################################


def dataset_load_and_save():
    """
    we make the connection to postgres using the psycopg2 library, create
    the schema to hold our covid data, and insert from the local csv file
    """

    path = os.getcwd()
    print(path)
    new_path = path + '/upload-data'
    print(new_path)
    onlyfiles = [f for f in listdir(new_path) if isfile(join(new_path, f))]
    print(onlyfiles)

    start = time.time()
    df_full = dt.fread(f"{new_path}/df.jay").to_pandas()
    print(df_full.shape)
    end = time.time()

    print("Read csv with chunks: ", (end - start), "sec")

    print(df_full.sample(10))

    print(get_db_url(CONN_ID))

    # connecting to a PostgreSQL database
    db = dataset.connect(get_db_url(CONN_ID))

    # get a reference to the table 'df'
    table = db['reports']

    db.begin()

    try:
        table.insert_many(rows=df_full.to_dict('records'), chunk_size=10000)
        db.commit()
    except:
        db.rollback()

    print(db.tables)


with DAG(dag_id=DAG_ID,
         default_args=WORKFLOW_DEFAULT_ARGS,
         description='Upload data from files to DB',
         schedule_interval="@once",
         catchup=False
         ) as dag:
    start_operator = DummyOperator(task_id='Begin_execution', dag=dag)

    dataset_load_and_save = PythonOperator(
        task_id="dataset_load",
        python_callable=dataset_load_and_save
    )

    end_operator = DummyOperator(task_id='Stop_execution')

    # DAG dependencies
    start_operator >> dataset_load_and_save >> end_operator
