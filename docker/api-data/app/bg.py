import os
import argparse

from cassandra_client import CassandraClient
from hdfs_client import HdfsClient

def main():

    #parser
    parser = argparse.ArgumentParser(description='Copy files from local to hdfs')
    parser.add_argument('id',  metavar='id', type=str, help='the dataset id')
    parser.add_argument('fid', metavar='fid', type=str, help='the file id')

    args = parser.parse_args()

    #connect to cassandra and hdfs
    c = CassandraClient('autoscience', 'cassandra')
    h = HdfsClient('hdfs')

    #very simple security rule:
    results = c.get('links', 1, {'from_tb':'datasets','from_id':args.id, 'to_tb':'files', 'to_id':args.fid}, 'to_id')
    if not results: return 'not found'

    #check file status
    results = c.get('files', 1, {'id':args.fid}, 'filename', 'hdfs', 'status')
    if not results: return 'not found'

    # push it to hdfs, if not there yet
    if results[0]['status']!='local': return 'transfer in progress'

    #todo: check for pid
    fullpath = os.path.join('/data',args.id,results[0]['filename'])
    dirname = os.path.dirname(fullpath)

    results = c.get('files', 1, {'id':args.fid}, 'status')
    if not results: return
    if results[0]['status'] != 'local': return

    # We can now upload the data
    h.client.makedirs(dirname)

    # write file
    hdfs_path = h.client.upload(fullpath, fullpath, overwrite=True)
    c.modify('files', {'id':args.fid}, {'hdfs':'hdfs://hdfs-nn/' + hdfs_path, 'status':'hdfs'})

    #todo: update the record

if __name__ == '__main__':
    main()
