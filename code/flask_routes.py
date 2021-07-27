from os import name
from flask import Flask, Response
import json

import json_file_handler as j

app = Flask(__name__)
@app.route('/discord_status')
def discord_status():
    response = j.read()
    return response

@app.route('/healthz/ready')
def readiness():
    data = j.read(namespace='metadata')['ready']
    status_code = 200 if data == "OK" else 500
    status_response = {"status": f"{data}"}
    response = Response(json.dumps(status_response), status=status_code, mimetype='application/json')
    return response

@app.route('/healthz/live')
def liveness():
    data = j.read(namespace='metadata')['live']
    status_code = 200 if data == "OK" else 500
    status_response = {"status": f"{data}"}
    response = Response(json.dumps(status_response), status=status_code, mimetype='application/json')
    return response