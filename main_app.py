import app.app as app
import api.api_service as api
from flask import Flask

if __name__ == '__main__':
    server = Flask(__name__)
    app.init_dash_app(server)
    api.init_api(server)
    server.run(debug=True, host='0.0.0.0',port=5578)