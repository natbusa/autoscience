# cassandra driver
from cassandra.cluster import Cluster
from cassandra.cluster import SimpleStatement, ConsistencyLevel

class CassandraClient:
  def __init__(self):

    self.cluster = Cluster(['cassandra'])
    self.session = self.cluster.connect()

    cql_stmt = """
      CREATE KEYSPACE IF NOT EXISTS autoscience
      WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1' };
    """
    result = self.session.execute(cql_stmt)

    cql_stmt = """
      CREATE TABLE IF NOT EXISTS autoscience.files (
        id        text,
        filename  text,
        url       text,
        hdfs      text,
        status    text,
        PRIMARY KEY (id)
      );
    """
    result = self.session.execute(cql_stmt)

    cql_stmt = """
      CREATE TABLE IF NOT EXISTS autoscience.counters (
        k   text,
        id  text,
        PRIMARY KEY (k)
      );
    """
    result = self.session.execute(cql_stmt)

    cql_stmt = """
      CREATE TABLE IF NOT EXISTS autoscience.links (
        from_tb text,
        from_id text,
        to_tb   text,
        to_id   text,
        PRIMARY KEY ((from_tb, from_id), to_tb, to_id)
      );
    """
    result = self.session.execute(cql_stmt)
