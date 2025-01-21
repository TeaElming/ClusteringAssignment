# clustering_methods/hierarchical_clustering.py
from models.blog import Blog
from models.cluster import Cluster
from distances.pearson_correlation import PearsonCorrelation


class HierarchicalClustering:
  def __init__(self, blogs):
    """
    Initialize the HierarchicalClustering instance.
    :param blogs: List of Blog instances to cluster
    """
    self.blogs = blogs
    self.pearson = PearsonCorrelation()

  def fit(self):
    """
    Perform hierarchical clustering on the provided blogs.
    :return: Root Cluster of the hierarchical clustering tree
    """
    # Initialize clusters: each blog is its own cluster
    clusters = [Cluster(blog=blog) for blog in self.blogs]

    while len(clusters) > 1:
      min_distance = None
      closest_pair = (0, 0)

      # Compute distances between all pairs of clusters
      for i in range(len(clusters)):
        for j in range(i + 1, len(clusters)):
          cluster_a = clusters[i]
          cluster_b = clusters[j]

          # Compute distance between clusters
          distance = self.compute_distance(cluster_a, cluster_b)

          if min_distance is None or distance < min_distance:
            min_distance = distance
            closest_pair = (i, j)

      # Merge the two closest clusters
      i, j = closest_pair
      cluster_a = clusters[i]
      cluster_b = clusters[j]

      new_cluster = self.merge_clusters(cluster_a, cluster_b, min_distance)

      # Remove the old clusters and add the new cluster
      clusters.pop(max(i, j))  # Remove the cluster with the higher index first
      clusters.pop(min(i, j))
      clusters.append(new_cluster)

    # Return the root cluster
    return clusters[0]

  def compute_distance(self, cluster_a, cluster_b):
    """
    Compute the Pearson correlation distance between two clusters.
    :param cluster_a: First Cluster
    :param cluster_b: Second Cluster
    :return: Distance between the two clusters
    """
    # Get average word frequencies for both clusters
    avg_word_freqs_a = cluster_a.get_average_word_frequencies()
    avg_word_freqs_b = cluster_b.get_average_word_frequencies()

    # Create temporary Blog instances with average word frequencies
    blog_a = Blog(blog_name="tempA", word_frequencies=avg_word_freqs_a)
    blog_b = Blog(blog_name="tempB", word_frequencies=avg_word_freqs_b)

    # Compute Pearson correlation
    distance = self.pearson.pearson_correlation(blog_a, blog_b)

    return distance

  def merge_clusters(self, cluster_a, cluster_b, distance):
    """
    Merge two clusters into a new parent cluster.
    :param cluster_a: First Cluster to merge
    :param cluster_b: Second Cluster to merge
    :param distance: Distance between the two clusters
    :return: New parent Cluster
    """
    new_cluster = Cluster(left=cluster_a, right=cluster_b, distance=distance)

    # Set parent pointers
    cluster_a.parent = new_cluster
    cluster_b.parent = new_cluster

    # Sum word frequencies and update blog count
    new_cluster.total_word_frequencies = self.sum_word_frequencies(
      cluster_a.total_word_frequencies, cluster_b.total_word_frequencies
    )
    new_cluster.blog_count = cluster_a.blog_count + cluster_b.blog_count

    return new_cluster

  @staticmethod
  def sum_word_frequencies(freqs_a, freqs_b):
    """
    Sum the word frequencies from two clusters.
    :param freqs_a: Word frequencies from the first cluster
    :param freqs_b: Word frequencies from the second cluster
    :return: Summed word frequencies
    """
    total_freqs = {}
    words = set(freqs_a.keys()).union(freqs_b.keys())
    for word in words:
      total_freqs[word] = freqs_a.get(word, 0) + freqs_b.get(word, 0)
    return total_freqs

  def print_cluster(self, cluster, indent=0):
    """
    Recursively print the cluster hierarchy.
    :param cluster: Cluster to print
    :param indent: Indentation level
    """
    print('  ' * indent, end='')
    if cluster.blog is not None:
      # Leaf node
      print(cluster.blog.blog_name)
    else:
      # Internal node
      print('-')
      if cluster.left is not None:
        self.print_cluster(cluster.left, indent + 1)
      if cluster.right is not None:
        self.print_cluster(cluster.right, indent + 1)

  def write_cluster_to_json(self, cluster):
    """
    Convert the cluster hierarchy to a JSON-serializable format.
    :param cluster: Cluster to convert
    :return: JSON-serializable representation of the cluster
    """
    if cluster.blog is not None:
      # Leaf node
      return {'name': cluster.blog.blog_name}
    else:
      # Internal node
      return {
        'left': self.write_cluster_to_json(cluster.left) if cluster.left else None,
        'right': self.write_cluster_to_json(cluster.right) if cluster.right else None,
        'distance': cluster.distance
      }
