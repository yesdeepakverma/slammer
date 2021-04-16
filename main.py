import logging
import os
from flask import Flask
from router import add_route


app = Flask(__name__)
add_route(app)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    PORT = int(os.getenv('PORT') or 8080)
    DEBUG = bool(os.getenv('DEBUG')) or True
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)