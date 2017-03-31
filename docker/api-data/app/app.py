from flask import Flask, make_response, request
from flask import url_for, redirect

from werkzeug.utils import secure_filename

import json

import os
import sys
import subprocess

from cassandra_client import CassandraClient
from hdfs_client import HdfsClient

c = CassandraClient()
h = HdfsClient()

app = Flask(__name__,static_url_path='/files', static_folder='/data')

app.config['UPLOAD_FOLDER'] = '/data'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #max 16 MB

def output_jsonapi(data, code, headers=None):
  resp = make_response(json.dumps(data), code)
  resp.headers.extend(headers or {})
  resp.headers['content-type']='application/vnd.api+json'
  return resp

@app.route('/datasets/<id>/files', methods=['POST', 'GET'])
def upload_file(id):
  if request.method == 'POST':
    # check if the post request has the file part
    if 'file' not in request.files:
      return 'not allowed'

    # for multiple files use:
    files = request.files.getlist("file")

    # if user does not select file, browser also
    # submit a empty part without filename
    if not files:
      return 'No selected file'

    stored_files = []
    for file in files:
      #some very basic os precautions :)
      filename = secure_filename(file.filename)
      filepath = os.path.join(app.config['UPLOAD_FOLDER'], id)

      # check if dataset directory is there, if not create it.
      os.makedirs(filepath,exist_ok=True)

      #file fullname
      fullname = os.path.join(filepath, filename)

      #save the file
      file.save(fullname)
      stored_files.append(fullname)

      #store record
      fid = c.new_id("files")
      record = {
        'id': fid,
        'filename':filename,
        'hdfs': '',
        'status': 'local'
      }
      c.insert("files",record)

      #link to dataset
      record = {
        'from_tb': 'datasets',
        'from_id': id,
        'to_tb'  : 'files',
        'to_id'  : fid
      }
      c.insert("links",record)

    return str(stored_files)

  else: # handle default 'GET'
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], id)
    items = os.listdir(filepath) if os.path.isdir(filepath) else []
    data = [ {'attributes': {'filename': v}} for v in items]
    return json.dumps({'data':data})

@app.route('/datasets/<id>/files/<fid>/raw')
def serve_rawdata(id, fid):

  #get the linked file id
  results = c.get('links', ['to_id'], {'from_tb':'datasets','from_id':id}, 1)

  if not results:
    return 'not such dataset'

  results = c.get('files', ['filename', 'hdfs', 'status'], {'id':fid}, 1)

  if results:
    return redirect(url_for('static', filename='{}/{}'.format(id,results[0]['filename'])))
  else:
    return []

@app.route('/')
def root_path():
  return 'hello data repo!'

# now let's serve some crud resources
# serve application/vnd.api+json as response content-type header

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
