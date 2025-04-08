import os

# API ENDPOINT
api_host = os.getenv('API_HOST','192.168.0.88')
api_port = os.getenv('API_PORT','5002')

api_endpoint = f"http://{api_host}:{api_port}"

# SPOKE ENPOINT
spoke_host = os.getenv('SPOKE_HOST','192.168.0.121')
spoke_port = os.getenv('SPOKE_PORT',3000)

spoke_endpoint = f"http://{spoke_host}:{spoke_port}"
