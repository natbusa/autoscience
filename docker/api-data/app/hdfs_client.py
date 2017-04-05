from hdfs import Config

class HdfsClient:
  def __init__(self, profile):
    self.client = Config().get_client(profile)
