class HierarchicalVisualisation extends HTMLElement {
  async connectedCallback() {
    try {
      // Fetch the hierarchical data
      const response = await fetch(`http://127.0.0.1:5000/hierarchical`)
      const { result } = await response.json() // Extract the `result` key

      // Clear any existing content
      this.innerHTML = ""

      // Set up container
      const container = document.createElement("div")
      container.style.width = "100%"
      container.style.height = "1000px" // Increased height
      container.style.overflow = "auto"
      container.style.border = "1px solid #ccc"
      this.appendChild(container)

      // Append SVG
      const svg = d3
        .select(container)
        .append("svg")
        .attr("width", "100%")
        .attr("height", 1000) // Increased height
        .append("g")
        .attr("transform", "translate(50, 50)")

      // Load and render tree
      this.container = container
      this.svg = svg
      this.data = result

      // Create root and expand all nodes
      this.root = d3.hierarchy(this.data, (d) =>
        [d.left, d.right].filter(Boolean)
      )
      this.root.descendants().forEach((d) => {
        d._children = null
      })

      this.renderTree()

      // Add resize listener
      window.addEventListener("resize", () => this.renderTree())
    } catch (error) {
      console.error("Error rendering tree:", error)
    }
  }

  renderTree() {
    // Calculate container width
    const width = this.container.clientWidth
    const height = 1000 // Increased height

    // Update SVG dimensions
    d3.select(this.svg.node().parentNode).attr("width", width)

    // Create tree layout
    const treeLayout = d3.tree().size([height - 100, width - 200])

    // Layout the tree
    treeLayout(this.root)

    // Clear previous elements
    this.svg.selectAll("*").remove()

    // Render links
    const linkGroup = this.svg.append("g").attr("class", "links")
    linkGroup
      .selectAll("path")
      .data(this.root.links())
      .enter()
      .append("path")
      .attr(
        "d",
        d3
          .linkHorizontal()
          .x((d) => d.y)
          .y((d) => d.x)
      )
      .style("fill", "none")
      .style("stroke", "#ccc")
      .style("stroke-width", 1.5)

    // Render nodes
    const nodeGroup = this.svg.append("g").attr("class", "nodes")
    const node = nodeGroup
      .selectAll("g")
      .data(this.root.descendants())
      .enter()
      .append("g")
      .attr("class", "node")
      .attr("transform", (d) => `translate(${d.y}, ${d.x})`)
      .on("click", (event, d) => {
        if (d.children) {
          d._children = d.children
          d.children = null
        } else {
          d.children = d._children
          d._children = null
        }
        this.renderTree() // Re-render tree
      })

    node
      .append("circle")
      .attr("r", 5)
      .style("fill", (d) =>
        d.children || d._children ? "steelblue" : "lightgreen"
      )

    node
      .append("text")
      .attr("dx", (d) => (d.children ? -10 : 10))
      .attr("dy", 3)
      .style("text-anchor", (d) => (d.children ? "end" : "start"))
      .text((d) => d.data.name || "")
  }
}

customElements.define("hierarchical-visualisation", HierarchicalVisualisation)
