import psycopg2

from pathlib import Path
from dotenv import load_dotenv
import os

CURRENT_DIR = Path(__file__).resolve().parent
load_dotenv(CURRENT_DIR / "conection_db.env")
dbname = os.getenv("dbname")
user = os.getenv("user")
password = os.getenv("password")
host = os.getenv("host")
port = os.getenv("port")


#dbname = "mydb"
#user = "postgres"
#password = "postgres"
#host = "localhost"
#port = 5432


try:
    # connection = psycopg2.connect(database="dbname", user="username",
    # password="pass", host="hostname", port=5432)
    connection = psycopg2.connect(
        database=dbname,
        user=user,
        password=password,
        host=host,
        port=port,
    )

    cursor = connection.cursor()
    print("¡Connected to the database!")

    # close the connection

    cursor.close()
    connection.close()

except psycopg2.OperationalError:
    print("Unable to connect to the database.")
