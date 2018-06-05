from flask import Flask
from flask_restful import Resource

from api import  init_api
import  settings
from dao import init_db

app = Flask(__name__)

#配置app
app.config.from_object(settings.Config)
#初始化API
init_api(app)
#初始化dao，或db
init_db(app)



if __name__ == '__main__':
    app.run()
