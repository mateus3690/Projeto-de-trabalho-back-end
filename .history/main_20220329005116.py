import repackage
repackage.up()

from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from src.Controller.controllerCalendario import DirectCalendario, DirectCalendarioPass
from Controller.controllerFechamento import DirectFechamento
#from restMethod.restAuth import DirectAuth, DirectAuthPass
from Controller.controllerLogin import DirectLogin, DirectLoginPass


app = Flask(__name__)
CORS(app)
api = Api(app)


api.add_resource(DirectCalendario, '/v1/pontos/<string:chave>/<string:registro>/' )
api.add_resource(DirectCalendarioPass, '/v1/pontos/' )

api.add_resource(DirectLogin, '/v1/login/<string:email>/<string:senha>/')
api.add_resource(DirectLoginPass, '/v1/login/')

api.add_resource(DirectFechamento, '/v1/fechamento/<string:chave>/<string:mes>/')
# api.add_resource(DirectAuth, '/v1/usuarios/<int:id>/' )
# api.add_resource(DirectAuthPass, '/v1/usuarios/' )


if __name__ == '__main__':
     app.run(debug=True)

     