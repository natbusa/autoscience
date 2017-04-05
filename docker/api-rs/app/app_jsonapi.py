from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException

from flask import Flask, request, make_response
from flask import abort as flask_abort, _app_ctx_stack

import collections

DATABASE = {
    'ideas': {
        '0': {
            'title': 'amy',
            'desc': 'dances',
        },
        '1': {
            'title': 'bob',
            'desc': 'writes',
        },
        '2': {
            'title': 'sue',
            'desc': 'runs',
        },
        '3': {
            'title': 'joe',
            'desc': 'sings',
        },
        '4': {
            'title': 'Ada',
            'desc': 'thinks',
        }
    },
    'links': {
        'ideas/0/ideas/4': {},
        'ideas/0/ideas/2': {},
        'ideas/1/ideas/3': {},
        'ideas/2/ideas/0': {}
    }
}

import json


app = Flask(__name__)


# custom abort
def abort(status_code, message=None, headers=None):
    """ Json error response. """
    body = {'error': {'status': status_code, 'title': message}}
    flask_abort(make_response(json.dumps(body), status_code, headers))


# the json error for exceptions
def make_json_error(ex):
    body = {'error': {'status': ex.code, 'title': str(ex)}}
    status = ex.code if isinstance(ex, HTTPException) else 500
    return make_response(json.dumps(body), status)


# intercept all standard execptions
for code in default_exceptions:
    app.register_error_handler(code, make_json_error)


def connect_to_database():
    global DATABASE
    return DATABASE


def get_db():
    """Connects the database"""
    top = _app_ctx_stack.top
    if not hasattr(top, 'db'):
        top.db = connect_to_database()
    return top.db


@app.teardown_appcontext
def close_database(exception):
    """Closes the database again at the end of the request."""
    top = _app_ctx_stack.top
    if hasattr(top, 'db'):
        pass
        # top.db.close()


@app.before_request
def before_request():
    if not request.is_json:
        abort(406, 'Content-Type in request must be application/vnd.api+json')


@app.after_request
def after_request(resp):
    resp.headers['content-type'] = 'application/vnd.api+json'
    return resp

import re
class Tree(dict):
    """Implementation of perl's autovivification feature."""
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value
    
def get_relationships(from_type=None, from_id=None, to_type=None, to_id=None):
    db = get_db()
    
    #select * from _links where from_type= ...
    filter = '/'.join([str(key) if key else '\w+' for key in [from_type, from_id, to_type, to_id]])
    regex = re.compile('^{}$'.format(filter))
    ids = [e.group(0) for e in [regex.match(i) for i in db['links'].keys()] if e]
    d = Tree()
    for id in ids:
        r = id.split('/')
        d[r[0]][r[1]][r[2]]=r[3]
        if db['links'][id]: d[r[0]][r[1]][r[2]][r[3]] = db['links'][id]

    # relationships
    return dict(d)

def jsonapi_relationships(resource_relationships):
    relationships = Tree()
    for from_type, v1 in resource_relationships.items():
        for from_id, v2 in v1.items():
            for to_type, v3 in v2.items():
                relationships[to_type]['links']['self'] = '/{}/{}/relationships/{}'.format(from_type,from_id,to_type)
                relationships[to_type]['links']['related'] = '/{}/{}/{}'.format(from_type,from_id,to_type)
                relationships[to_type]['data'] = [ {'type':to_type, 'id': id} for id in v3.keys()]
                
    return relationships

def jsonapi_resource(resource_type, id, resource_attributes=None, resource_relationships=None):
    resource = {'id': id, 'type': resource_type }
    if resource_attributes: resource['attributes'] = resource_attributes
    if resource_relationships: resource['relationships'] = jsonapi_relationships(resource_relationships)
    return resource

def jsonapi_render(data, code=200):
    body = {'data':data}
    return json.dumps(body), code

RESOURCE = 'ideas'

@app.route('/' + RESOURCE + '/<id>', methods=['GET'])
def get_resource(id):
    db = get_db()
    if id not in db[RESOURCE]:
        abort(404, 'Resource not found')
    resource_attributes = db[RESOURCE][id]
    resource_relationships = get_relationships(RESOURCE, id)
    resource = jsonapi_resource(RESOURCE, id, resource_attributes, resource_relationships)
    return jsonapi_render(resource)


@app.route('/' + RESOURCE, methods=['GET'])
def get_collection():
    db = get_db()

    collection = []
    
    for id in db[RESOURCE].keys():
        resource_attributes = db[RESOURCE][id]
        resource_relationships = get_relationships(RESOURCE,id)
        resource = jsonapi_resource(RESOURCE, id, resource_attributes, resource_relationships)
        collection.append(resource)
        
    return jsonapi_render(collection)

@app.route('/' + RESOURCE + '/<id>', methods=['DELETE'])
def delete_resource(id):
    db = get_db()
    del db[RESOURCE][id]
    return '', 204


from datetime import datetime


def parse_attributes(resource):
    # mapping here ... (if required)
    return resource['data'].get('attributes', {})


def validate_resource(resource, post=True):
    # validate
    check = True
    
    if ('data' not in resource) or \
            ('id' not in resource['data'] and not post) or \
            ('type' not in resource['data']):
        check = False
    
    if post:
        if 'attributes' not in resource['data']:
            check = False
        else:
            # check all attributes are there
            for i in ['title', 'desc']:
                if (i not in resource['data']['attributes']):
                    check = False
                    break
    
    return check

def update(d, u):
    if u:
        for k, v in u.items():
            if isinstance(v, collections.Mapping):
                r = update(d.get(k, {}), v)
                d[k] = r
            else:
                d[k] = u[k]
    return d


def build_attributes(post_attributes, patch_attributes=None):
    # extract/build
    item = post_attributes
    if patch_attributes:
        item = update(item, patch_attributes)

    # decorate
    ts = datetime.utcnow().timestamp()
    item['created'] = ts
    item['modified'] = ts
    return item


@app.route('/' + RESOURCE + '/<id>', methods=['PATCH'])
def patch_resource(id):
    db = get_db()
    if id not in db[RESOURCE]:
        abort(404, 'Resource not found')

    # parse json
    resource = request.get_json()
    if not validate_resource(resource, False):
        abort(400, 'Resource did not validate')
    
    patch_attributes = parse_attributes(resource)

    # patch/build resource attributes
    resource_attributes = build_attributes(db[RESOURCE][id], patch_attributes)
    
    # save
    db[RESOURCE][id] = resource_attributes
    
    resource = jsonapi_resource(RESOURCE, id, resource_attributes)
    return jsonapi_render(resource)


@app.route('/' + RESOURCE, methods=['POST'])
def post_resource():
    db = get_db()
    collection = db[RESOURCE]

    # get id
    id = str(int(max(collection.keys() or ['-1'])) + 1)
    
    # parse json
    resource = request.get_json()
    if not validate_resource(resource):
        abort(400, 'Resource did not validate')
    
    post_attributes = parse_attributes(resource)
    
    # patch/build resource attributes
    resource_attributes = build_attributes(post_attributes)

    # save
    db[RESOURCE][id] = resource_attributes
    
    resource = jsonapi_resource(RESOURCE, id, resource_attributes)
    return jsonapi_render(resource, 201)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

