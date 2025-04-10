import common,config
import requests, json # type: ignore
from flask import Flask, session, render_template
import base64

import logwriter,os

current_directory = os.getcwd()
logger = logwriter.Writer(current_directory + "/logs/","gui",__name__)

def get_response(url: str):
    token = session.get('Token')
    if not token:
        return {'status_code': 401, 'error': 'Unauthorized'}
    
    try:
        response = requests.get(f'{config.api_endpoint}{url}',
                            headers={"accept": "application/json",
                                    "Authorization":f"Bearer {token}"})
        data = response.json()
        
        if response.status_code != 200:
            logger.logs(data)
            session.clear()
            return {'status_code': response.status_code, 'error': data['detail']}
        
        response_data = data['data'] if 'data' in data else data
        return {'status_code': response.status_code, 'data': response_data}
        
    except requests.exceptions.RequestException as e:
        logger.logs(str(e))
        return {'status_code': 500, 'error': str(e)}

def get_user_avatar():
     # Token disimpan dalam session atau mana-mana tempat yang sesuai
    token = session.get("Token")

    if not token:
        logger.logs("No token found in session")
        return None

    # Panggil API FastAPI
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    try:
        response = requests.get(f"{config.api_endpoint}/api/avatar", headers=headers)

        if response.status_code == 200:
            # Convert binary image ke base64 string
            image_base64 = base64.b64encode(response.content).decode('utf-8')
            return image_base64
        else:
            # return f"Gagal ambil avatar: {response.status_code}", 400
            logger.logs(f"Gagal ambil avatar: {response.status_code}")
            return None
    except Exception as e:
        logger.logs(f"Exception: {str(e)}")
        return None
    
def put_response(url: str, payload: dict):
    token = session.get('Token')
    if not token:
        return {'status_code': 401, 'error': 'Unauthorized'}
    
    try:
        response = requests.put(f'{config.api_endpoint}{url}',
                            headers={"accept": "application/json",
                                    "Authorization":f"Bearer {token}",
                                    "Content-Type":"application/json"},
                            data=json.dumps(payload))
        data = response.json()
        
        if response.status_code != 200:
            logger.logs(data)
            session.clear()
            return {'status_code': response.status_code, 'error': data['detail']}
        
        response_data = data['data'] if 'data' in data else data
        return {'status_code': response.status_code, 'data': response_data}
        
    except requests.exceptions.RequestException as e:
        logger.logs(str(e))
        return {'status_code': 500, 'error': str(e)}      
    
def delete_response(url: str):
    token = session.get('Token')
    if not token:
        return {'status_code': 401, 'error': 'Unauthorized'}
    
    try:
        response = requests.delete(f'{config.api_endpoint}{url}',
                            headers={"accept": "application/json",
                                    "Authorization":f"Bearer {token}"})
        data = response.json()
        
        if response.status_code != 200:
            logger.logs(data)
            session.clear()
            return {'status_code': response.status_code, 'error': data['detail']}
        
        response_data = data['data'] if 'data' in data else data
        return {'status_code': response.status_code, 'data': response_data}
        
    except requests.exceptions.RequestException as e:
        logger.logs(str(e))
        return {'status_code': 500, 'error': str(e)}  
        
def post_response(url: str, payload: dict):
    token = session.get('Token')
    if not token:
        return {'status_code': 401, 'error': 'Unauthorized'}
    
    try:
        response = requests.post(f'{config.api_endpoint}{url}',
                            headers={"accept": "application/json",
                                    "Authorization":f"Bearer {token}",
                                    "Content-Type":"application/json"},
                            data=json.dumps(payload))
        data = response.json()
        
        if response.status_code != 200:
            logger.logs(data)
            session.clear()
            return {'status_code': response.status_code, 'error': data['detail']}
        
        response_data = data['data'] if 'data' in data else data
        return {'status_code': response.status_code, 'data': response_data}
        
    except requests.exceptions.RequestException as e:
        logger.logs(str(e))
        return {'status_code': 500, 'error': str(e)}
    
def get_response_spoke(url: str):
    token = session.get('Token')
    if not token:
        return {'status_code': 401, 'error': 'Unauthorized'}
    
    try:
        response = requests.get(f'{config.spoke_endpoint}{url}',
                            headers={"accept": "application/json"})
        data = response.json()
        
        if response.status_code != 200:
            logger.logs(data)
            session.clear()
            return {'status_code': response.status_code, 'error': data['detail']}
        
        response_data = data['data'] if 'data' in data else data
        return {'status_code': response.status_code, 'data': response_data}
        
    except requests.exceptions.RequestException as e:
        logger.logs(str(e))
        return {'status_code': 500, 'error': str(e)}
    
