from flask import Flask, make_response, request
from flask import url_for, redirect

from werkzeug.utils import secure_filename

import json

import os
import sys
import subprocess

from cassandra_client import CassandraClient
from hdfs_client import HdfsClient

c = CassandraClient('autoscience', 'cassandra')
h = HdfsClient('hdfs')

app = Flask(__name__,static_url_path='/files', static_folder='/data')

app.config['UPLOAD_FOLDER'] = '/data'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #max 16 MB

def output_jsonapi(data, code=200, headers=None):
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

      #store record: get fresh new id
      try:
        fid = c.new_id("files")
      except ValueError:
        return 0

      #store record: build the object
      record = {
        'id': fid,
        'filename':filename,
        'url': '/api/data/datasets/{}/files/{}/local'.format(id,fid),
        'hdfs' : '',
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

      #push it to hdfs, if not there yet
      subprocess.Popen(
        ['nohup', 'python', './bg.py', id, fid],
        stdout=sys.stdout,
        stderr=sys.stderr,
        preexec_fn=os.setpgrp)

    return str(stored_files)

  else: # handle default 'GET'
    #very simple security rule:
    results = c.get('links', 100, {'from_tb':'datasets','from_id':id, 'to_tb':'files'}, 'to_id')

    data =[]
    for item in results:
      rows = c.get('files', 1, {'id':item['to_id']}, 'filename', 'url', 'hdfs', 'status', 'id')
      if rows: data.append({'attributes':rows[0]})

    return output_jsonapi({'data':data})

@app.route('/datasets/<id>/files/<fid>/local')
def serve_rawdata(id, fid):

  #very simple security rule:
  results = c.get('links', 1, {'from_tb':'datasets','from_id':id, 'to_tb':'files', 'to_id':fid}, 'to_id')
  if not results: return 404

  #check file status
  results = c.get('files', 1, {'id':fid}, 'filename', 'url', 'hdfs', 'status')
  if not results: return 404

  if results:
    return redirect(url_for('static', filename='{}/{}'.format(id,results[0]['filename'])))
  else:
    return redirect(url_for('/'))

@app.route('/datasets/<id>/files/<fid>/hdfs')
def serve_hdfsdata(id, fid):

  #very simple security rule:
  results = c.get('links', 1, {'from_tb':'datasets','from_id':id, 'to_tb':'files', 'to_id':fid}, 'to_id')
  if not results: return 404

  #check file status
  results = c.get('files', 1, {'id':fid}, 'filename', 'hdfs', 'status')
  if not results: return 404

  # push it to hdfs, if not there yet
  if results[0]['status']=='local':
    subprocess.Popen(['nohup', './bg.py', id, fid], stdout=sys.stdout, stderr=sys.stderr, preexec_fn=os.setpgrp)

  return redirect(url_for('static', filename='{}/{}'.format(id,results[0]['filename'])))

@app.route('/')
def root_path():
  return 'hello data repo!'

# now let's serve some crud resources
# serve application/vnd.api+json as response content-type header

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
