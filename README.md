# Clustering Algorithms on Blog Data

## Overview

This project implements clustering algorithms (K-means and Hierarchical Clustering) to analyse and group blogs from a dataset containing 99 blogs. The goal is to explore similarities among the blogs using Pearson similarity and visualise the clustering results in an interactive format.

The system supports:

* K-means Clustering with configurable stopping criteria
* Hierarchical Clustering with tree-based visualisation
* RESTful API for server-client interaction

This project is suitable for educational and practical purposes in data clustering and visualisation.

## Features

1. K-means Clustering:
* Uses Pearson similarity for distance measurement.
* Supports configurable stopping criteria:
  * Stop after a fixed number of iterations.
  * Stop when no new assignments are made.
* Presents results as a list of clusters and their assignments.
2. Hierarchical Clustering:
* Uses Pearson similarity for linkage.
* Outputs results as an interactive tree with expandable/collapsible branches in the GUI.
3. RESTful API:
* Allows clients to send clustering requests.
* Returns JSON-formatted results to be rendered in a client-side GUI.
4. Frontend Visualisation:
* Displays K-means results as cluster lists.
* Visualises Hierarchical Clustering results as an interactive tree.

## Getting Started

### Prerequisites
* Python 3.8+
* Flask for the backend
* A modern browser for the frontend GUI
* Additional dependencies listed in requirements.txt

### Installation
1. Clone the repository:
`````
git clone https://github.com/username/clustering-algorithms.git
cd clustering-algorithms
`````
2. Install dependencies:
`````
pip install -r requirements.txt
`````
3. Start the backend server:
`````
python app.py
`````
4. Open the frontend in your browser:
`````
http://localhost:3000
`````

## API Reference

### Endpoints
* /kmeans
  * Method: POST
  * Description: Executes K-means clustering on the blog dataset.
  * Request Parameters:
    * clusters (int): Number of clusters.
    * iterations (int, optional): Maximum number of iterations.
  * Response Format:
````
{
  "clusters": [
    {
      "id": 1,
      "blogs": ["Blog1", "Blog2"]
    },
    {
      "id": 2,
      "blogs": ["Blog3", "Blog4"]
    }
  ]
}
````
* /hierarchical
  * Method: POST
  * Description: Executes Hierarchical Clustering on the blog dataset.
  * Request Parameters:
    * linkage (string, optional): Type of linkage (default: Pearson).
  * Response Format:
````
{
  "tree": {
    "name": "Root",
    "children": [
      {
        "name": "Cluster1",
        "children": [
          {"name": "Blog1"},
          {"name": "Blog2"}
        ]
      }
    ]
  }
}
````
## Usage
* Run K-means Clustering:
  * Submit a POST request to /kmeans with the number of clusters and iterations.
  * View the cluster assignments in the frontend.
* Run Hierarchical Clustering:
  * Submit a POST request to /hierarchical.
  * Explore the interactive tree visualisation in the frontend.

## Test Cases
### K-means

K-means may yield different results between runs due to random initialisation. Example output:


### Hierarchical

Hierarchical clustering produces deterministic results. Example tree visualisation:


## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix:
`git checkout -b feature-name`
3. Commit your changes:
`git commit -m "Add feature-name"`
4. Push to your branch:
`git push origin feature-name`
5. Submit a pull request.


## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

Created as a submission for an assignment on the Web Intelligence course at Linnaeus University.