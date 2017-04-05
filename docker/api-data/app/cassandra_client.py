# cassandra driver
import time

from cassandra.cluster import Cluster, NoHostAvailable
from cassandra.query import dict_factory

class CassandraClient:
    def __init__(self, keyspace, *seednodes):

        while True:
            try:
                self.cluster = Cluster(seednodes)
                self.session = self.cluster.connect(keyspace)
                break
            except NoHostAvailable:
                print("Waiting ... connecting to cassandra")
                time.sleep(1)


        self.session.row_factory = dict_factory

        self.debug = True

    def debug(self,value):
        self.debug = value

    def s(self,v):
      # quote strings, not numbers!
      return "'{}'".format(v) if isinstance(v, str) else v

    def q(self,template, *args):
        # quote strings, not numbers!
        a = template.split('{}')
        q = [isinstance(v, str) for v in args]

        s = a[0]
        for i in range(len(q)):
            s += "'{}'" if q[i] else "{}"
            s += a[i+1]

        return s.format(*args)

    def get(self,table, limit, cond, *columns):
        # which cols?
        cols = ', '.join(columns)

        # render query
        where_array = [ k + '=' + self.s(v) for k,v in cond.items()]
        where = ' AND '.join(where_array)

        # the mighty cql query
        cql_stmt = "SELECT {} FROM {} WHERE {} LIMIT {};".format(cols, table, where, limit)
        if self.debug: print(cql_stmt)

        # execute
        resultSet = self.session.execute(cql_stmt)
        return list(resultSet)

    def insert(self,table, d):
        # which cols?
        cols = ', '.join(d.keys())
        vals = ', '.join(self.s(v) for v in d.values())

        # the mighty cql query
        cql_stmt = "INSERT INTO {} ({}) VALUES ({});".format(table,cols,vals)
        if self.debug: print(cql_stmt)

        # execute
        result = self.session.execute(cql_stmt)

    def modify(self,table, cond, d):
        # render query
        where_array = [ k + '=' + self.s(v) for k,v in cond.items()]
        where = ' AND '.join(where_array)

        # what to set?
        set_zip = zip(d.keys(), [self.s(v) for v in d.values()])
        set_list = ['{}={}'.format(k,v) for (k, v) in set_zip]
        set = ', '.join(set_list)

        # the mighty cql query
        cql_stmt = "UPDATE {} SET {} WHERE {};".format(table,set,where)
        if self.debug: print(cql_stmt)

        # execute
        result = self.session.execute(cql_stmt)

    def cas(self,table, cond, field, old, new):
        # render query
        where_array = [ k + '=' + self.s(v) for k,v in cond.items()]
        where = ' AND '.join(where_array)

        # cas operation in cassandra using paxos
        cql_stmt = 'UPDATE {} SET {} = '.format(table, field)
        cql_stmt += self.s(new)
        cql_stmt += ' WHERE {} IF {} = '.format(where, field)
        cql_stmt += self.s(old) + ';'
        if self.debug: print(cql_stmt)

        # execute
        rows = self.session.execute(cql_stmt)
        return rows[0]['[applied]']

    def new_id(self,key):
        #default start
        new_value='0'

        # get current counter value
        results = self.get('counters', 1, {'k': key}, 'id')

        if results:
            old_value    = results[0]['id']
            new_value = str(int(old_value)+1)

            success = self.cas('counters', {'k':key}, 'id', old_value, new_value)

            if not success:
                raise ValueError("no id generated")
        else:
            self.insert('counters', {'k': key, 'id': new_value})

        return new_value


