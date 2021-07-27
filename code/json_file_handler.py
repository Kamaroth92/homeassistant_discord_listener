import json
from json.decoder import JSONDecodeError
from pathlib import Path

import envvar_handler as e
import rest_api_handler as r

default_values = """
    {
        "metadata": {
            "ready": "BAD",
            "live": "BAD",
            "post_flag": "False",
            "discord_connected": "False",
            "homeassistant_connected": "False"
        },
        "data": {
            "user": "False",
            "muted": "False",
            "deafened": "False",
            "camera_enabled": "False",
            "stream_enabled": "False",
            "afk": "False",
            "connected_to_channel": "False"
        }
    }
"""
temp_file_name = e.return_var('TMP_FILE')
def load(file_name = temp_file_name):
    json_file = Path(file_name)
    if not json_file.exists():
        json_file.touch()
        
    try:
        with json_file.open() as f:
            data = json.load(f)
            return data
    except JSONDecodeError:
        return json.loads(default_values)

def delete(file_name = temp_file_name):
    json_file = Path(file_name)
    if json_file.exists():
        json_file.unlink()

def read(file_name = temp_file_name, namespace="data", load_all_values=False):
    json_data = load(file_name)
    if load_all_values:
        return json_data
    else:
        return json_data[namespace]

def write(key, value, file_name = temp_file_name, namespace="data", post_data=True):
    json_data = read(file_name, load_all_values=True)
    if json_data[namespace][key] != value:
        json_data[namespace][key] = value
        json_file = Path(file_name)
        with json_file.open("w") as f:
            f.write(json.dumps(json_data))
        if post_data and namespace == 'data':
            r.set_post_flag(True)
