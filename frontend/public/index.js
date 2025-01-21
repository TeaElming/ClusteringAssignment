import "./components/dropdown.js"
import "./components/hierchicalVisualisation.js"
import "./components/clusterVisualisation.js"

document.addEventListener("DOMContentLoaded", () => {
  const dropdown = document.querySelector("drop-down-options")
  const representationDiv = document.getElementById("RepresentationDiv")

  dropdown.shadowRoot
    .querySelector("#method-select")
    .addEventListener("change", (event) => {
      const selectedMethod = event.target.value

      // Clear previous visualisation
      representationDiv.innerHTML = ""

      if (selectedMethod === "hierchical") {
        // Dynamically insert the HierarchicalVisualisation component
        const hierarchicalVisualisation = document.createElement(
          "hierarchical-visualisation"
        )
        representationDiv.appendChild(hierarchicalVisualisation)
      } else if (selectedMethod === 'kmeans') {
        const kmeansClusterVisualisation = document.createElement("cluster-visualisation")
        // Set the data-url attribute
        kmeansClusterVisualisation.setAttribute(
          "data-url",
          "http://127.0.0.1:5000/kmeans"
        )
        representationDiv.appendChild(kmeansClusterVisualisation)
      } else if (selectedMethod === 'kmeansopt') {
        const kmeansClusterVisualisationOpt = document.createElement("cluster-visualisation")
        // Set the data-url attribute
        kmeansClusterVisualisationOpt.setAttribute(
          "data-url",
          "http://127.0.0.1:5000/kmeans-optimised"
        )
        representationDiv.appendChild(kmeansClusterVisualisationOpt)
      }
      else {
        representationDiv.innerHTML = `<p>The selected method "${selectedMethod}" is not yet implemented.</p>`
      }
    })

  // Enable the dropdown after DOM content is loaded
  dropdown.shadowRoot.querySelector("#method-select").disabled = false
})
