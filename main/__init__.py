# import logging

# import azure.functions as func
# from flask import Flask, request, redirect

# app = Flask(__name__)

# def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
#     """Each request is redirected to the WSGI handler.
#     """
#     return func.WsgiMiddleware(app.wsgi_app).handle(req, context)

# @app.route("/")
# def index():
#     logging.info('Python HTTP trigger function processed a request.')
   
#     return redirect("https://github.com/Azure-Samples/flask-app-on-azure-functions/", code=302)
#     #return func.HttpResponse(vscode_redirect, status_code=302)



#LOADING THE LIBRARIES
import os,shutil,glob
import slack
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slackeventsapi import SlackEventAdapter
from pathlib import Path              #to load environment variable
from dotenv import load_dotenv        #to load environment variable
import mysql.connector as mysql
import numpy as np
import pandas as pd
import requests                       #to obtain the payload text
import sys
import getopt
#datetime imports
from datetime import date
from datetime import datetime as dt
from datetime import timedelta as delta
from datetime import timedelta
import numexpr
#FLASK
from flask import Flask, request, Response
from threading import Thread 
import json
import base64
import seaborn as sns
import plotly.graph_objects as go
import plotly
import plotly.io as pio
import plotly.offline as pyo
from plotly.subplots import make_subplots
import plotly.express as px
from PIL import Image
import matplotlib.dates as mdates
import matplotlib
import scipy.signal
import warnings
from vis_functions import *
from slack.signature import SignatureVerifier



#os.environ
#setting the path to environment variable (.env file) and loading it
#this is done to protect the slack_bot_token 
env_path = Path('.') / '.env'
load_dotenv(dotenv_path = env_path)

app = Flask(__name__)

slack_event_adapter = SlackEventAdapter(
    os.environ['SIGNING_SECRET'], '/slack/events', app)

#getting slack_bot_token from our stored environment variable
client = WebClient(token=os.environ['SLACK_TOKEN'])
#obtains bot id
BOT_ID = client.api_call("auth.test")['user_id'] #gives us the bot id

signature_verifier = SignatureVerifier(os.environ["SIGNING_SECRET"])


    
def backgroundworker(text,response_url):
    ending_message = "Process executed successfully"
    
    client.chat_postMessage(channel='#asb_dd_top10_changes', 
                                            text=f"{ending_message}"
                                            )
    

#files_list trigger slash command
@app.route('/files_list1', methods=['POST'])
def files_trigger():
    data = request.form
    data2 = request.form.to_dict()
    #print(data)
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')
    text = data.get('text')
    response_url = data.get("response_url")
    #event = payload.get('event', {})
    #text = event.get('text')
    greeting_message = "Processing your request. Please wait."
    ending_message = "Process executed successfully"

    
    thr = Thread(target=backgroundworker, args=[text,response_url])
    thr.start()
    
    client.chat_postMessage(channel='#asb_dd_top10_changes', 
                                            text=f"{greeting_message}"
                                            )
    
    return f'{text}', 200

if __name__ == "__main__":
    app.run(debug=True) #debug = True, makes sure if we modify this file we don't need to rerun the python script
