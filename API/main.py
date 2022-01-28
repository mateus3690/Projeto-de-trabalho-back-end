import repackage
repackage.up()

from flask import Flask
from flask_restful import Api
from restMethod.restCalendario import DirectCalendario, DirectCalendarioPass
from restMethod.restAuth import DirectAuth, DirectAuthPass
from restMethod.restLogin import DirectLogin, DirectLoginPass


app = Flask(__name__)
api = Api(app)


api.add_resource(DirectCalendario, '/v1/pontos/<string:registro>/' )
api.add_resource(DirectCalendarioPass, '/v1/pontos/' )

api.add_resource(DirectAuth, '/v1/usuarios/<int:id>/' )
api.add_resource(DirectAuthPass, '/v1/usuarios/' )

api.add_resource(DirectLogin, '/v1/login/<string:email>/<string:senha>/')
api.add_resource(DirectLoginPass, '/v1/login/')

if __name__ == '__main__':
     app.run(debug=True)

     