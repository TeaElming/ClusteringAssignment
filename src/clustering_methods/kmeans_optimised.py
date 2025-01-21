import random
import json
from models.blog import Blog
from models.centroid import Centroid
from distances.pearson_correlation import PearsonCorrelation


class KMeansClusteringOptimised:
  def __init__(self, blogs, k):
    self.blogs = blogs
    self.k = k
    self.centroids = []
    self.assignments = {}  # Blog name to cluster index
    self.pearson = PearsonCorrelation()
    self.iterations = 0  # Track the number of iterations

  def initialize_centroids(self):
    # Randomly select k blogs as initial centroids
    initial_blogs = random.sample(self.blogs, self.k)
    for blog in initial_blogs:
      # Create a centroid with the same word frequencies
      centroid = Centroid(blog.word_frequencies.copy())
      self.centroids.append(centroid)

  def assign_blogs_to_centroids(self):
    self.assignments = {}
    for blog in self.blogs:
      distances = []
      for idx, centroid in enumerate(self.centroids):
        # Create a dummy blog object for centroid
        centroid_blog = Blog(
          blog_name=f"Centroid{idx}", word_frequencies=centroid.word_frequencies
        )
        distance = self.pearson.pearson_correlation(blog, centroid_blog)
        distances.append((distance, idx))
      # Assign the blog to the centroid with the smallest distance
      _, min_idx = min(distances)
      self.assignments[blog.blog_name] = min_idx

  def update_centroids(self):
    centroids_changed = False
    for idx, centroid in enumerate(self.centroids):
      # Get all blogs assigned to this centroid
      assigned_blogs = [
        blog for blog in self.blogs if self.assignments[blog.blog_name] == idx
      ]
      if assigned_blogs:
        # Update the centroid with new frequencies
        old_frequencies = centroid.word_frequencies.copy()
        centroid.update(assigned_blogs)
        if old_frequencies != centroid.word_frequencies:
          centroids_changed = True
    return centroids_changed

  def fit(self):
    self.initialize_centroids()
    while True:
      self.iterations += 1
      prev_assignments = self.assignments.copy() # Comparing it to the old assignment
      self.assign_blogs_to_centroids()
      centroids_changed = self.update_centroids()

      # Check for convergence: no centroid changes and assignments are stable
      if not centroids_changed and prev_assignments == self.assignments:
        print(f"Converged after {self.iterations} iterations.")
        break

  def get_clusters(self):
    clusters = {f"cluster_{i+1}": [] for i in range(self.k)}
    for blog_name, cluster_idx in self.assignments.items():
      clusters[f"cluster_{cluster_idx+1}"].append(blog_name)
    return clusters

  def get_clusters_json(self):
    clusters = self.get_clusters()
    return json.dumps(clusters, indent=2)

  def get_iterations(self):
    return self.iterations
