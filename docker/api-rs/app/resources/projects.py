from flask_restful import Resource
from flask_restful import reqparse, abort

PROJECTS = {
  '0': {'project': 'build the API'},
  '1': {'project': 'get the data'},
  '2': {'project': 'machine learn!'}
}

def abort_if_project_doesnt_exist(project_id):
  if project_id not in PROJECTS:
    abort(404, message="Todo {} doesn't exist".format(project_id))

parser = reqparse.RequestParser()
parser.add_argument('project', type=str, location='json', required=True)

# Todo
# shows a single project item and lets you delete a project item
class Item(Resource):
  def get(self, project_id):
    abort_if_project_doesnt_exist(project_id)
    return PROJECTS[project_id]

  def delete(self, project_id):
    del PROJECTS[project_id]
    return '', 204

  def put(self, project_id):
    abort_if_project_doesnt_exist(project_id)
    args = parser.parse_args()
    project = {'project': args['project']}
    PROJECTS[project_id] = project
    return project, 201

class List(Resource):
  def get(self):
     return [  {'id':k, 'data':v } for k, v in PROJECTS.items() ]

  def post(self):
    args = parser.parse_args()
    project_id = int(max(PROJECTS.keys()).lstrip('project')) + 1
    project_id = 'project%i' % project_id
    PROJECTS[project_id] = {'project': args['project']}
    return PROJECTS[project_id], 201
