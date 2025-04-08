import common,config
import requests, json # type: ignore
from flask import Flask, session, render_template

import logwriter,os

current_directory = os.getcwd()
logger = logwriter.Writer(current_directory + "/logs/","gui",__name__)

def get_response(url: str):
    token = session.get('Token')
    if not token:
        return render_template("Login.html", error=response['Unauthorized'])
    try:
        response = requests.get(f'{config.api_endpoint}{url}',
                            headers={"accept": "application/json",
                                    "Authorization":f"Bearer {token}"})
        data = response.json()
        
        if response.status_code != 200:
            logger.logs(data)
            session.clear()
            return render_template("Login.html", error=response['detail'])
    
        response_data = data['data'] if 'data' in data else data
        return {'status_code': response.status_code, 'data': response_data}
        
    except requests.exceptions.RequestException as e:
        return render_template("Login.html", error=response['detail'])
    
    