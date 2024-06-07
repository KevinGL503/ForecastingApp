import app.app as app
import api.api_service as api
from flask import Flask
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()
HOST = os.getenv('RUN_HOST')
PORT = os.getenv('PORT')

if __name__ == '__main__':
    server = Flask(__name__)
    app.init_dash_app(server)
    api.init_api(server)
    server.run(debug=True, host=HOST,port=PORT)