
import os
from dotenv import load_dotenv

load_dotenv()

# --- Base de datos ---

REDSHIFT_HOST = 'warehouse-libgot.cgqrbtivohcq.us-east-1.redshift.amazonaws.com'
REDSHIFT_DB = 'warehouse'
REDSHIFT_USER = 'usuario_py'
REDSHIFT_PASSWORD = os.getenv("REDSHIFT_PASSWORD")
REDSHIFT_PORT = 5439

API_KEY = os.getenv("API_KEY")

# --- S3 ---
aws_access_key_id = os.getenv("aws_access_key_id")
aws_secret_access_key = os.getenv("aws_secret_access_key")


query = 'Select * from gold.ventas_arg WHERE fecha_creacion_loan BETWEEN %s AND %s limit 10'



# --- EMAIL ---
lista_email = ("aseverino@libgot.com","verrocchioc@libgot.com")


