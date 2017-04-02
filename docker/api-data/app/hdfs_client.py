from hdfs import Config

class HdfsClient:
  def __init__(self):
    self.client = Config().get_client('dev')
