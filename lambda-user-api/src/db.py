import psycopg2

DB_HOST = "host endpoint"
DB_NAME = "name"
DB_USER = "postgres"
DB_PASSWORD = "mypassword"

def get_db_connection():
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER, #master username on aws
            password=DB_PASSWORD, #db password
            port="5432", #db port 
        )
        print("Connected to RDS (PostgreSQL) successfully!")
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to RDS:", error)
        return None