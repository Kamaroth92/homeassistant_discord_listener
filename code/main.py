from os import name
from waitress import serve
from multiprocessing import Process

import flask_routes
import envvar_handler as e
import json_file_handler as j
import rest_api_handler as r
import ready_live_checks
from discord_handler import MyClient

discord_token = e.return_var('DISCORD_TOKEN')
webhook_port = e.return_var('WEBHOOK_PORT')
webhook_host = e.return_var('WEBHOOK_HOST')

client = MyClient()

def flask_server():
    serve(flask_routes.app, host=webhook_host, port=webhook_port)

def discord_listener():
    client.run(discord_token, bot=False)

def rest_api_handler_loop():
    r.loop()

def ready_live_check_loop():
    ready_live_checks.loop()

if __name__ == '__main__':
    j.delete()
    Process(target=flask_server).start()
    Process(target=discord_listener).start()
    Process(target=rest_api_handler_loop).start()
    Process(target=ready_live_check_loop).start()

