import examples
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class store_map(Resource):
    def get(self, food_list):
        return {'data': examples.main(food_list)}

api.add_resource(store_map, '/store_map/<food_list>')

if __name__ == '__main__':
     app.run(host= '0.0.0.0')
