from flask_restful import abort, Resource

from datetime import datetime

DATABASE = {
  'projects/0/datasets/4':{},
  'projects/0/datasets/2':{},
  'projects/2/datasets/4':{},
  'projects/3/datasets/1':{}
}

def abort_if_link_doesnt_exist(id):
  if id not in DATABASE:
    abort(404)

import re
def get_list(filter):
  if filter:
    regex = re.compile('^{}$'.format(filter))
    ids = [e.group(0) for e in [regex.match(i) for i in DATABASE.keys()] if e]
  else:
    ids = DATABASE.keys()
  return ids

# valid json api minimalistic in 6 lines of code
# see http://jsonapi.org/
def jsonapi_item(id, code=200):
  return {'data': {'id': id, 'type': 'links', 'attributes': DATABASE[id]}}, code

def jsonapi_list(filter, code=200):
  data = [{'id': id, 'type': 'links', 'attributes': DATABASE[id]} for id in get_list(filter)]
  return {'data': data}, code

class Item(Resource):
    def get(self, from_type, from_id, to_type, to_id):
        id = '/'.join([from_type, from_id, to_type, to_id])
        abort_if_link_doesnt_exist(id)
        return jsonapi_item(id)

    def delete(self, from_type, from_id, to_type, to_id):
        id = '/'.join([from_type, from_id, to_type, to_id])
        del DATABASE[id]
        return '', 204

    def put(self, from_type, from_id, to_type, to_id):
        id = '/'.join([from_type, from_id, to_type, to_id])

        # store
        DATABASE[id] = {}
        return jsonapi_item(id)

class List(Resource):
    def get(self, from_type='\w+', from_id='\w+', to_type='\w+', to_id='\w+'):
        filter = '/'.join([from_type, from_id, to_type, to_id])
        return jsonapi_list(filter)
