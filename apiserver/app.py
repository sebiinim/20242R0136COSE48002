import os
os.environ['CUDA_LAUNCH_BLOCKING'] = "1"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"



#get_ipython().system('pip install -q flask_restx')

from flask import Flask
from flask_restx import Resource, Api
from revision import Revision
from evaluation import Evaluation
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__, static_url_path='')
app.wsgi_app = ProxyFix(app.wsgi_app)

api = Api(app, version='1.0', title='Sanhak equalsum APIII', description='Swagger docs', doc='/docs')



api.add_namespace(Revision, '/revision')
api.add_namespace(Evaluation, '/evaluation')

if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0', port=13000)


