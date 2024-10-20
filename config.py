import os


# Database
user = os.environ['POSTGRES_USER']
password = os.environ['POSTGRES_PASSWORD']
host = os.environ['POSTGRES_HOST']
database = os.environ['POSTGRES_DB']
port = os.environ['POSTGRES_PORT']

DATABASE_CONNECTION_URI = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'

# API ENDPOINT

api_host = os.environ['API_HOST']
api_port = os.environ['API_PORT']

api_endpoint = f"http://{api_host}:{api_port}"