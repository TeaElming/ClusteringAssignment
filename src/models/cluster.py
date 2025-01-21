class Cluster:
  cluster_count = 0  # Class variable to keep track of clusters

  def __init__(self, blog=None, left=None, right=None, distance=0.0, id=None):
    if id is None:
      id = Cluster.cluster_count
      Cluster.cluster_count += 1

    self.blog = blog  # For leaf nodes, this is the Blog object
    self.left = left  # Left child cluster
    self.right = right  # Right child cluster
    self.distance = distance  # Distance between left and right clusters
    self.id = id  # Unique identifier for the cluster
    self.parent = None  # Parent cluster

    if blog is not None:
      # Leaf node: initialize with the blog's word frequencies
      self.total_word_frequencies = blog.word_frequencies.copy()
      self.blog_count = 1
    else:
      # Internal node: will be set when merging clusters
      self.total_word_frequencies = {}
      self.blog_count = 0

  def get_average_word_frequencies(self):
    """
    Calculate the average word frequencies for the cluster.
    :return: Dictionary of average word frequencies
    """
    return {
      word: freq / self.blog_count
      for word, freq in self.total_word_frequencies.items()
    }
