import requests
import json
from time import sleep

import envvar_handler as e
import json_file_handler as j

homeassistant_uri = e.return_var('HOMEASSISTANT_URI')
homeassistant_token = e.return_var('HOMEASSISTANT_TOKEN')

last_post_data = None

def check_home_assistant_connection():
    headers = {
        'Authorization': f'Bearer {homeassistant_token}', 
        'Content-Type': 'application/json'
    }
    status = 'False'
    
    try:
        r = requests.get(f'{homeassistant_uri}/api/', headers=headers)
        message = json.loads(r.content)['message']
        if message == "API running.":
            status = 'True'
    except:
        status = 'False'

    j.write('homeassistant_connected', f'{status}', namespace='metadata')
    if status == 'True':
        return True
    else:
        return False



def set_post_flag(value):
    j.write('post_flag', str(value), namespace="metadata")

def post_flag_set():
    data = j.read(namespace='metadata')
    return True if data['post_flag'] == "True" else False

def post_data_to_homeassistant(body):
    headers = {
        'Authorization': f'Bearer {homeassistant_token}', 
        'Content-Type': 'application/json'
    }
    
    payload = {
        "state": f"{'connected' if body['connected_to_channel'] == 'True' else 'disconnected'}",
        "attributes": body
    }
    r = requests.post(f'{homeassistant_uri}/api/states/sensor.discord_listener', headers=headers, data=json.dumps(payload))
    set_post_flag(False)

def loop():
    global last_post_data
    while True and check_home_assistant_connection():
        current_data = j.read()
        if post_flag_set() or last_post_data != current_data:
            post_data_to_homeassistant(current_data)
            last_post_data = current_data
        else:
            sleep(0.2)
