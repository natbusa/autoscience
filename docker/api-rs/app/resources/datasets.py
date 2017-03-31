from flask_restful import abort, Resource

from datetime import datetime

DATABASE = {
  '0': {
    'title': 'Iris',
    'desc':  'data data data, flowers flowers, flowers',
    'created': datetime(2007, 12, 6, 15, 29).timestamp(),
    'modified': datetime(2007, 12, 9, 18, 45).timestamp()
  }
}

import collections

def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.Mapping):
      r = update(d.get(k, {}), v)
      d[k] = r
    else:
      d[k] = u[k]
  return d

def abort_if_project_doesnt_exist(id):
  if id not in DATABASE:
    abort(404)

# valid json api minimalistic in 6 lines of code
# see http://jsonapi.org/

def jsonapi_item(id):
  return {'id': id, 'type': 'projects', 'attributes': DATABASE[id]}

def jsonapi_list(filter=''):
  items = [  jsonapi_item(k) for k in DATABASE.keys() ]
  return items

def jsonapi(id=None, code=200):
  data = jsonapi_item(id) if id else jsonapi_list()
  return {'data':data}, code

from flask import request

def parse_data():
  args = request.get_json()
  data = args['data']['attributes']
  item = {
    'title': data['title'],
    'desc' : data['desc']
  }
  return item

class Item(Resource):
  def get(self, id):
    abort_if_project_doesnt_exist(id)
    return jsonapi(id)

  def delete(self, id):
    del DATABASE[id]
    return '', 204

  def put(self, id):
    abort_if_project_doesnt_exist(id)

    # build object
    item = update(DATABASE[id],parse_data())
    ts = datetime.utcnow().timestamp()
    item['modified'] = ts

    # store
    DATABASE[id] = item
    return jsonapi(id)

class List(Resource):
  def get(self):
    return jsonapi()

  def post(self):
    #get id
    id = str(int(max(DATABASE.keys() or ['-1'])) + 1)

    # build object
    item = parse_data()
    ts = datetime.utcnow().timestamp()
    item['created']  = ts
    item['modified'] = ts

    # store
    DATABASE[id] = item
    return jsonapi(id, 201)
