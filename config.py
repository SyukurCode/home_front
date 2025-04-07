import os


# Database
# user = os.getenv('POSTGRES_USER','admin')
# password = os.getenv('POSTGRES_PASSWORD','syukur123***')
# host = os.getenv('POSTGRES_HOST','192.168.0.88')
# database = os.getenv('POSTGRES_DB','homeapi')
# port = os.getenv('POSTGRES_PORT',5432)

# DATABASE_CONNECTION_URI = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'

# API ENDPOINT
api_host = os.getenv('API_HOST','192.168.0.88')
api_port = os.getenv('API_PORT','5002')

api_endpoint = f"http://{api_host}:{api_port}"

# SPOKE ENPOINT
spoke_host = os.getenv('SPOKE_HOST','192.168.0.121')
spoke_port = os.getenv('SPOKE_PORT',3000)

spoke_endpoint = f"http://{spoke_host}:{spoke_port}"

# RADIS
# redis_host = os.environ['REDIS_HOST']
# redis_port = os.environ['REDIS_PORT']