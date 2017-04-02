# cassandra driver
from cassandra.cluster import Cluster
from cassandra.query import dict_factory
from cassandra.cluster import SimpleStatement, ConsistencyLevel

class CassandraClient:
  def __init__(self):

    self.cluster = Cluster(['cassandra'])
    self.session = self.cluster.connect()
    self.session.row_factory = dict_factory

  def new_id(self,key):
    success = False
    results = self.get('counters', ['id'], {'k':key}, 1)

    #default start
    new_value='0'

    if results:
      old_value  = results[0]['id']
      new_value = str(int(old_value)+1)

      success = self.cas('counters', {'k':key}, 'id', old_value, new_value)

      if not success:
        raise ValueError("no id generated")
    else:
      self.insert('counters', {'k':key, 'id':new_value})

    return new_value

  def cas(self,table, cond, field, old, new):
    # render query
    where_array = [ "{}='{}'".format(k, v) if isinstance(v, str) else "{}={}".format(k, v) for k,v in cond.items()]
    where = ' AND '.join(where_array)

    # the mighty cql query
    cql_stmt = "UPDATE autoscience.{} SET {} = '{}' WHERE {} IF {} = '{}'".format(table,field, new, where, field, old)

    rows = self.session.execute(cql_stmt)
    return rows[0]['[applied]']

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
