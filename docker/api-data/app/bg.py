# cassandra driver
from cassandra.cluster import Cluster
from cassandra.cluster import SimpleStatement, ConsistencyLevel

cluster = Cluster('cassandra')
session = cluster.connect()

model = {
  '(intercept)': 48.,
  'first_feature': 2.,
  'second_feature': 12.,
}

from hdfs import Config
client = Config().get_client('dev')

# First, we delete any existing `models/` folder on HDFS.
client.delete('models', recursive=True)

# We can now upload the data, first as CSV.
client.makedirs('models/try/now')

# This is equivalent to the JSON example above.
from json import dumps
client.write('model1.json', dumps(model))

with client.read('model1.json', encoding='utf-8', delimiter='\n') as reader:
  for line in reader:
    print(line)
