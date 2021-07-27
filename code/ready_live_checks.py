from os import name
from time import sleep

import json_file_handler as j
import rest_api_handler as r
import envvar_handler as e


def check_ready():
    status = []
    data = j.read(namespace='metadata')

    ## Discord checks
    discord_token = e.return_var('DISCORD_TOKEN')
    if discord_token == "" or discord_token is None:
        status.append('missing discord token')
    else:
        if data['discord_connected'] != "True":
            status.append('discord not connected')
    
    ## Home assistant checks
    r.check_home_assistant_connection()
    homeassistant_token = e.return_var('HOMEASSISTANT_TOKEN')
    if homeassistant_token == "" or homeassistant_token is None:
        status.append('missing home assistant token')
    else:
        if data['homeassistant_connected'] != "True":
            status.append('homeassistant not connected')

    if len(status) == 0:
        j.write('ready', 'OK', namespace='metadata')
    else:
        j.write('ready', ', '.join(status), namespace='metadata')

        

def check_live():
    data = j.read(namespace='metadata')
    status = []

    ## Discord checks
    if data['discord_connected'] != "True":
        status.append('discord not connected')
    
    ## Homeassistant checks
    if data['homeassistant_connected'] != "True":
        status.append('homeassistant not connected')
    
    if len(status) == 0:
        j.write('live', 'OK', namespace='metadata')
    else:
        j.write('live', ', '.join(status), namespace='metadata')

def loop():
    while True:
        if j.read(namespace='metadata')['ready'] != "OK":
            check_ready()
            sleep(0.2)
        else:
            check_live()
            sleep(1)