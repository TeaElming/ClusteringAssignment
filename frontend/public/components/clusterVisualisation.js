class ClusterVisualisation extends HTMLElement {
  constructor() {
    super()
    this.attachShadow({ mode: "open" })
  }

  connectedCallback() {
    this.render()
    const dataUrl = this.getAttribute("data-url") // Fetch the URL from an attribute
    if (dataUrl) {
      this.fetchData(dataUrl)
    } else {
      console.error(
        "No data-url attribute provided for ClusterVisualisation component."
      )
      this.shadowRoot.innerHTML += `<p>Error: No data URL specified for the component.</p>`
    }
  }

  async fetchData(url) {
    try {
      const response = await fetch(url)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const data = await response.json()
      this.createDropdowns(data.result)
    } catch (error) {
      console.error("Error fetching data:", error)
      this.shadowRoot.innerHTML += `<p>Error loading clusters: ${error.message}</p>`
    }
  }

  createDropdowns(clusters) {
    const container = this.shadowRoot.querySelector("#dropdown-container")

    for (const [clusterName, items] of Object.entries(clusters)) {
      // Create dropdown container
      const dropdown = document.createElement("div")
      dropdown.className = "dropdown"

      // Create dropdown button
      const button = document.createElement("button")
      button.textContent = clusterName
      button.className = "dropdown-button"
      button.addEventListener("click", () => {
        list.style.display = list.style.display === "none" ? "block" : "none"
      })

      // Create dropdown list
      const list = document.createElement("ul")
      list.className = "dropdown-list"
      list.style.display = "none"

      items.forEach((item) => {
        const listItem = document.createElement("li")
        listItem.textContent = item
        list.appendChild(listItem)
      })

      dropdown.appendChild(button)
      dropdown.appendChild(list)
      container.appendChild(dropdown)
    }
  }

  render() {
    this.shadowRoot.innerHTML = `
      <style>
        .dropdown {
          margin: 10px 0;
        }
        .dropdown-button {
          background-color: #007bff;
          color: white;
          padding: 10px 15px;
          border: none;
          cursor: pointer;
        }
        .dropdown-button:hover {
          background-color: #0056b3;
        }
        .dropdown-list {
          list-style: none;
          margin: 0;
          padding: 0;
          border: 1px solid #ccc;
          max-height: 200px;
          overflow-y: auto;
        }
        .dropdown-list li {
          padding: 8px 12px;
          cursor: pointer;
          background-color: #f9f9f9;
        }
        .dropdown-list li:hover {
          background-color: #e9ecef;
        }
      </style>
      <div id="dropdown-container" class="dropdown-container"></div>
    `
  }
}

customElements.define("cluster-visualisation", ClusterVisualisation)
