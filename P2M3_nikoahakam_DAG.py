# =============================================================================
# Name : Niko Amrullah Hakam
# Batch : FTDS - RMT - 038
# =============================================================================

import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from airflow import DAG
from airflow.decorators import task
from airflow.operators.empty import EmptyOperator
from airflow.models import Variable
from elasticsearch import Elasticsearch


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 11, 1, 9, 10),  # 1st of November 2024, 09:10 AM
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    'data_cleaning_pipeline',
    default_args=default_args,
    description='Pipeline to clean and load data to Elasticsearch',
    schedule_interval='10,20,30 9 * * 6',  # Every Saturday, between 09:10 AM and 09:30 AM
    catchup=False
) as dag:

    start = EmptyOperator(task_id='start')
    end = EmptyOperator(task_id='end')

    @task()
    def fetch_from_postgresql():
        # Connect to PostgreSQL and fetch raw data
        database = "airflow"
        username = "airflow"
        password = "airflow"
        host = "postgres"

        postgres_url = f"postgresql+psycopg2://{username}:{password}@{host}/{database}"
        engine = create_engine(postgres_url)

        query = "SELECT * FROM table_m3"
        df = pd.read_sql(query, engine)
        df.to_csv('/opt/airflow/dags/raw_data.csv', index=False)
        print("Data fetched from PostgreSQL successfully!")

    @task()
    def data_cleaning():
        # Read the raw data
        df = pd.read_csv('/opt/airflow/dags/raw_data.csv')
        
        # Standardize column names
        df.columns = [col.lower().replace(' ', '_').strip().replace('-', '_').replace('.', '') for col in df.columns]
        
        # Perform cleaning steps
        ## Remove duplicates
        df.drop_duplicates(inplace=True)  
        
        ## missing values handling
        ### Fill numerical columns with the mean
        df.select_dtypes(include=['float64', 'int64']).fillna(df.mean(), inplace=True) # either with mean of df or with 0

        ### Fill categorical columns with 'N/A'
        df.select_dtypes(include=['object']).fillna('N/A', inplace=True)

        # Save cleaned data
        df.to_csv('/opt/airflow/dags/cleaned_data.csv', index=False)
        print("Data cleaning completed!")

    
    @task()
    def insert_to_db():
        database = "airflow"
        username = "airflow"
        password = "airflow"
        host = "postgres"

        postgres_url = f"postgresql+psycopg2://{username}:{password}@{host}/{database}"

        engine = create_engine(postgres_url)
        conn = engine.connect()

        df = pd.read_csv('/opt/airflow/dags/cleaned_data.csv')

        df.to_sql('data_superstore', conn, index=False, if_exists='replace')
        print("Success INSERT")
        
        
    @task()
    def post_to_elasticsearch():
        # Connect to Elasticsearch
        es = Elasticsearch([{'host': 'elasticsearch', 'port': 9200}])  # Use 'elasticsearch' if running in Docker
        
        # Check if Elasticsearch is connected
        if not es.ping():
            raise ValueError("Connection to Elasticsearch failed!")

        # Load the cleaned data
        file_path = '/opt/airflow/dags/cleaned_data.csv'
        try:
            df = pd.read_csv(file_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found at {file_path}")

        # Index data into Elasticsearch
        index_name = 'cleaned_data'
        for i, row in df.iterrows():
            # Convert the row to a dictionary and index it in Elasticsearch
            doc = row.to_dict()
            es.index(index=index_name, id=i, body=doc)

        print(f"Data posted to Elasticsearch successfully into index '{index_name}'")

    # Define task dependencies
    start >> fetch_from_postgresql() >> data_cleaning() >> insert_to_db() >> post_to_elasticsearch() >> end
    
    
    
    
    # =============================================================================
    # Trial and Error
    
    # @task()
    # def post_to_elasticsearch():
    #     # Connect to Elasticsearch
    #     es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

    #     # Load the cleaned data
    #     df = pd.read_csv('/opt/airflow/dags/cleaned_data.csv')

    #     # Index data into Elasticsearch
    #     for i, row in df.iterrows():
    #         es.index(index='cleaned_data', id=i, body=row.to_dict())
    #     print("Data posted to Elasticsearch successfully!")