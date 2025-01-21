import time
import pandas as pd
import json

from models.blog import Blog
from clustering_methods.hierchical_clustering import HierarchicalClustering
from clustering_methods.kmeans_clustering import KMeansClustering
from clustering_methods.kmeans_optimised import KMeansClusteringOptimised

class Runner:
  def __init__(self, data_file):
    self.blogs = self._load_data(data_file)

  def _load_data(self, file_path):
    """
    Load the blog data from a tab-separated text file and create Blog objects.
    :param file_path: Path to the data file.
    :return: List of Blog objects.
    """
    df = pd.read_csv(file_path, delimiter='\t')
    blogs = []
    for _, row in df.iterrows():
      blog_name = row[0]  # Assume the first column is the blog name
      word_frequencies = row[1:].to_dict()  # Remaining columns are word frequencies
      blogs.append(Blog(blog_name=blog_name, word_frequencies=word_frequencies))
    return blogs

  def hierarchical(self):
    """
    Perform hierarchical clustering on the blogs.
    :return: JSON object containing time taken and the clustering result.
    """
    start_time = time.time()
    hierarchical_clustering = HierarchicalClustering(self.blogs)
    root_cluster = hierarchical_clustering.fit()
    end_time = time.time()

    # Convert the hierarchical clustering result to JSON
    clustering_result = hierarchical_clustering.write_cluster_to_json(root_cluster)

    print(json.dumps({
      "time_ms": (end_time - start_time) * 1000,
      "result": clustering_result
    }, indent=2))

  def kmeans(self, k, max_iterations=100):
    """
    Perform k-means clustering on the blogs.
    :param k: Number of clusters.
    :param max_iterations: Maximum number of iterations.
    :return: JSON object containing time taken, iterations, and clustering result.
    """
    start_time = time.time()
    kmeans_clustering = KMeansClustering(self.blogs, k, max_iterations=max_iterations)
    kmeans_clustering.fit()
    end_time = time.time()

    print(json.dumps({
      "time_ms": (end_time - start_time) * 1000,
      "iterations": kmeans_clustering.get_iterations(),
      "result": kmeans_clustering.get_clusters()
    }, indent=2))

  def kmeans_optimised(self, k):
    """
    Perform optimized k-means clustering on the blogs.
    :param k: Number of clusters.
    :return: JSON object containing time taken, iterations, and clustering result.
    """
    start_time = time.time()
    kmeans_optimised = KMeansClusteringOptimised(self.blogs, k)
    kmeans_optimised.fit()
    end_time = time.time()

    print(json.dumps({
      "time_ms": (end_time - start_time) * 1000,
      "iterations": kmeans_optimised.get_iterations(),
      "result": kmeans_optimised.get_clusters()
    }, indent=2))


if __name__ == "__main__":
  # Runner instance
  runner = Runner("blogdata.txt")

  # Example usage
  print("Hierarchical Clustering:")
  print(runner.hierarchical())

  print("\nK-Means Clustering (k=5, max_iterations=10):")
  print(runner.kmeans(k=5, max_iterations=10))

  print("\nOptimized K-Means Clustering (k=5):")
  print(runner.kmeans_optimised(k=5))