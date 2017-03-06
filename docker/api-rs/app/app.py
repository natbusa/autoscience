from flask import Flask
from flask_restful import Api
from resources import projects

app = Flask(__name__)
api = Api(app)

@app.route('/')
def hello_world():
    return 'Flask REST API with Flask-RESTful: check the <a href="projects">projects</a> !'

api.add_resource(projects.List, '/projects')
api.add_resource(projects.Item, '/projects/<project_id>')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
