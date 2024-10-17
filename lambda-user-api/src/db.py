import os
import psycopg2

def get_db_connection():
    try:
        # Fetch credentials from environment variables that we will be setting in serverless.yaml file
        DB_HOST = os.getenv('DB_HOST')
        DB_NAME = os.getenv('DB_NAME')
        DB_USER = os.getenv('DB_USER')
        DB_PASSWORD = os.getenv('DB_PASSWORD')
        DB_PORT = os.getenv('DB_PORT', '5432')

        # Create a connection
        connection = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        print("Connected to RDS (PostgreSQL) successfully!")
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to RDS:", error)
        return None
