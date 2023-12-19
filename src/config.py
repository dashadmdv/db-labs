import os
import dotenv

dotenv.load_dotenv('.env')

DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_NAME = os.environ.get('DB_NAME', 'med_center')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '12345678')
DB_PORT = os.environ.get('DB_PORT', '5432')
