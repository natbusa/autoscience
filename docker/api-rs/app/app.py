from flask import Flask, make_response
from flask_restful import Api

import json

app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Flask REST API with Flask-RESTful: check the <a href="projects">projects</a> !'

# now let's serve some crud resources
# serve application/vnd.api+json as response content-type header

def output_jsonapi(data, code, headers=None):
  resp = make_response(json.dumps(data), code)
  resp.headers.extend(headers or {})
  resp.headers['content-type']='application/vnd.api+json'
  return resp

class Api(Api):
  def __init__(self, *args, **kwargs):
    super(Api, self).__init__(*args, **kwargs)
    self.representations = {
      'application/vnd.api+json' : output_jsonapi,
      'application/json' : output_jsonapi
    }

api = Api(app)

from resources import ideas
api.add_resource(ideas.List, '/ideas', endpoint='/ideas')
api.add_resource(ideas.Item, '/ideas/<id>', endpoint='/ideas/<id>')

from resources import projects
api.add_resource(projects.List, '/projects', endpoint='/projects')
api.add_resource(projects.Item, '/projects/<id>', endpoint='/projects/<id>')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
