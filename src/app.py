import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from runner import Runner
import threading #Enables background processing.

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize Runner instance
runner = Runner("blogdata.txt")

# Global variables to store clustering results
hierarchical_results = None
kmeans_results = None
kmeans_optimised_results = None


# Preloading functions
def preload_hierarchical():
  """
  Preload hierarchical clustering results on app startup.
  """
  global hierarchical_results
  print("Starting hierarchical clustering preloading...")
  hierarchical_results = runner.hierarchical()
  print("Hierarchical clustering preloading completed.")


def preload_kmeans():
  """
  Preload k-means clustering results on app startup.
  """
  global kmeans_results
  print("Starting k-means clustering preloading...")
  kmeans_results = runner.kmeans(k=5, max_iterations=10)
  print("K-means clustering preloading completed.")


def preload_kmeans_optimised():
  """
  Preload optimized k-means clustering results on app startup.
  """
  global kmeans_optimised_results
  print("Starting optimized k-means clustering preloading...")
  kmeans_optimised_results = runner.kmeans_optimised(k=5)
  print("Optimized k-means clustering preloading completed.")


# Routes
@app.route("/", methods=["GET"])
def home():
  return "Hello"


@app.route("/hierarchical", methods=["GET"])
def hierarchical():
  """
  Route to fetch hierarchical clustering results.
  """
  global hierarchical_results
  if hierarchical_results is None:
    return jsonify({"status": "Processing", "message": "Hierarchical clustering is still being precomputed."}), 202
  return jsonify(json.loads(hierarchical_results))


@app.route("/kmeans", methods=["GET"])
def kmeans():
  """
  Route to fetch k-means clustering results.
  """
  global kmeans_results
  if kmeans_results is None:
    return jsonify({"status": "Processing", "message": "K-means clustering is still being precomputed."}), 202
  return jsonify(json.loads(kmeans_results))


@app.route("/kmeans-optimised", methods=["GET"])
def kmeans_optimised():
  """
  Route to fetch optimized k-means clustering results.
  """
  global kmeans_optimised_results
  if kmeans_optimised_results is None:
    return jsonify({"status": "Processing", "message": "Optimized k-means clustering is still being precomputed."}), 202
  return jsonify(json.loads(kmeans_optimised_results))


@app.route("/kmeans-rf", methods=["POST"])
def kmeans_refresh():
  """
  Route to refresh k-means clustering results.
  Accepts query parameters:
  - k (int): Number of clusters (default: 5)
  - iterations (int): Maximum number of iterations (default: 10)
  """
  global kmeans_results
  k = int(request.args.get("k", 5))
  iterations = int(request.args.get("iterations", 10))
  print("Refreshing k-means clustering...")
  kmeans_results = runner.kmeans(k=k, max_iterations=iterations)
  return jsonify({"status": "Success", "message": "K-means clustering refreshed."})


@app.route("/kmeans-optimised-rf", methods=["POST"])
def kmeans_optimised_refresh():
  """
  Route to refresh optimized k-means clustering results.
  Accepts query parameters:
  - k (int): Number of clusters (default: 5)
  """
  global kmeans_optimised_results
  k = int(request.args.get("k", 5))
  print("Refreshing optimized k-means clustering...")
  kmeans_optimised_results = runner.kmeans_optimised(k=k)
  return jsonify({"status": "Success", "message": "Optimized k-means clustering refreshed."})


if __name__ == "__main__":
  # Preload clustering results in separate threads
  threading.Thread(target=preload_hierarchical, daemon=True).start()
  threading.Thread(target=preload_kmeans, daemon=True).start()
  threading.Thread(target=preload_kmeans_optimised, daemon=True).start()

  # Run the Flask app
  app.run(debug=True)
