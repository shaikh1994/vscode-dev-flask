import logging

import azure.functions as func
from flask import Flask, request, redirect

app = Flask(__name__)

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    """Each request is redirected to the WSGI handler.
    """
    return func.WsgiMiddleware(app.wsgi_app).handle(req, context)

@app.route("/")
def index():
    logging.info('Python HTTP trigger function processed a request.')
   
    return redirect("https://github.com/Azure-Samples/flask-app-on-azure-functions/", code=302)
    #return func.HttpResponse(vscode_redirect, status_code=302)


