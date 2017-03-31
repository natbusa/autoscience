# cassandra driver
from cassandra.cluster import Cluster
from cassandra.query import dict_factory
from cassandra.cluster import SimpleStatement, ConsistencyLevel

class CassandraClient:
  def __init__(self):

    self.cluster = Cluster(['cassandra'])
    self.session = self.cluster.connect()
    self.session.row_factory = dict_factory

  def get_id(self,key):
    cql_stmt = "SELECT id from autoscience.counters where k='{}';".format(key)
    rows = self.session.execute(cql_stmt)
    if rows:
      return rows[0]['id']
    else:
      cql_stmt = "INSERT INTO autoscience.counters (id, k) VALUES (-1, '{}') IF NOT EXISTS;".format(key)
      result = self.session.execute(cql_stmt)
      return '-1'

  def new_id(self,key):
    success = False

    # infinite loop ahead
    while not success:
      id = self.get_id(key)
      new_id = str(int(id)+1)
      cql_stmt = "UPDATE autoscience.counters SET id = {} WHERE k='{}' IF id = {}".format(new_id, key, id)
      rows = self.session.execute(cql_stmt)
      success = rows[0]['[applied]']
      if success:
        return new_id

  def insert(self,table, d):
    # which cols?
    cols = ', '.join(d.keys())
    # quote strings, not numbers!
    vals = ', '.join("'{}'".format(v) if isinstance(v, str) else str(v) for v in d.values())
    # the mighty cql query
    cql_stmt = "INSERT INTO autoscience.{} ({}) VALUES ({});".format(table,cols,vals)
    result = self.session.execute(cql_stmt)

  def get(self,table, lst, cond, limit):
    # which cols?
    cols = ', '.join(lst)

    where_array = [ "{}='{}'".format(k, v) if isinstance(v, str) else "{}={}".format(k, v) for k,v in cond.items()]
    where = ' AND '.join(where_array)

    # the mighty cql query
    cql_stmt = "SELECT {} FROM autoscience.{} WHERE {} LIMIT {};".format(cols, table,where,limit)
    resultSet = self.session.execute(cql_stmt)
    return list(resultSet)
