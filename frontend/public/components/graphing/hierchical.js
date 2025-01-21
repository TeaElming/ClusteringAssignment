export default class HierarchicalGraph {
  constructor(data, container) {
    this.data = data // `response.result`
    this.container = container
    this.width = 800 // Width of the visible area
    this.height = 600 // Height of the visible area
    this.margin = { top: 20, right: 20, bottom: 20, left: 100 }
    this.render()
  }

  render() {
    // Clear any existing visualization
    d3.select(this.container).selectAll("*").remove()

    // Set up the scrollable SVG container
    const svg = d3
      .select(this.container)
      .append("svg")
      .attr("width", this.width)
      .attr("height", this.height)
      .append("g")
      .attr("transform", `translate(${this.margin.left},${this.margin.top})`)

    // Create a hierarchical data structure
    const root = d3.hierarchy(this.data, (d) =>
      d.left || d.right ? [d.left, d.right] : null
    )

    // Collapse all children by default
    root.descendants().forEach((d) => {
      if (d.depth && d.children) {
        d._children = d.children // Save collapsed children
        d.children = null // Hide children
      }
    })

    // Create a tree layout
    const tree = d3.tree().size([this.height - 100, this.width - 100])
    tree(root)

    this.svg = svg
    this.root = root
    this.tree = tree

    // Store initial positions
    root.x0 = this.height / 2
    root.y0 = 0

    // Render the graph
    this.update(root)
  }

  update(source) {
    const duration = 400

    // Compute the new tree layout
    const nodes = this.tree(this.root).descendants()
    const links = this.tree(this.root).links()

    // Normalize for fixed-depth
    nodes.forEach((d) => {
      d.y = d.depth * 200 // Adjust spacing between levels
    })

    // Update nodes
    const node = this.svg
      .selectAll("g.node")
      .data(nodes, (d) => d.id || (d.id = Math.random()))

    // Enter any new nodes at the parent's previous position
    const nodeEnter = node
      .enter()
      .append("g")
      .attr("class", "node")
      .attr("transform", (d) => `translate(${source.y0},${source.x0})`)
      .on("click", (event, d) => this.toggleChildren(d))

    nodeEnter
      .append("circle")
      .attr("r", 1e-6)
      .attr("fill", (d) => (d._children ? "#555" : "#fff"))
      .attr("stroke", "steelblue")
      .attr("stroke-width", 2)

    nodeEnter
      .append("text")
      .attr("dy", ".35em")
      .attr("x", (d) => (d.children || d._children ? -10 : 10))
      .style("text-anchor", (d) =>
        d.children || d._children ? "end" : "start"
      )
      .text((d) => d.data.name || d.data.distance?.toFixed(2))
      .style("cursor", "pointer")

    // Transition nodes to their new position
    const nodeUpdate = node
      .merge(nodeEnter)
      .transition()
      .duration(duration)
      .attr("transform", (d) => `translate(${d.y},${d.x})`)

    nodeUpdate
      .select("circle")
      .attr("r", 5)
      .attr("fill", (d) => (d._children ? "#555" : "#fff"))

    // Transition exiting nodes to the parent's new position
    const nodeExit = node
      .exit()
      .transition()
      .duration(duration)
      .attr("transform", (d) => `translate(${source.y},${source.x})`)
      .remove()

    nodeExit.select("circle").attr("r", 1e-6)

    nodeExit.select("text").style("fill-opacity", 1e-6)

    // Update the links
    const link = this.svg.selectAll("path.link").data(links, (d) => d.target.id)

    // Enter any new links at the parent's previous position
    const linkEnter = link
      .enter()
      .insert("path", "g")
      .attr("class", "link")
      .attr("d", (d) => {
        const o = { x: source.x0, y: source.y0 }
        return this.diagonal(o, o)
      })
      .attr("fill", "none")
      .attr("stroke", "#ccc")
      .attr("stroke-width", 2)

    // Transition links to their new position
    link
      .merge(linkEnter)
      .transition()
      .duration(duration)
      .attr("d", (d) => this.diagonal(d.source, d.target))

    // Transition exiting nodes to the parent's new position
    link
      .exit()
      .transition()
      .duration(duration)
      .attr("d", (d) => {
        const o = { x: source.x, y: source.y }
        return this.diagonal(o, o)
      })
      .remove()

    // Store the old positions for transition
    nodes.forEach((d) => {
      d.x0 = d.x
      d.y0 = d.y
    })
  }

  diagonal(s, d) {
    return `M${s.y},${s.x}
            C${(s.y + d.y) / 2},${s.x}
             ${(s.y + d.y) / 2},${d.x}
             ${d.y},${d.x}`
  }

  toggleChildren(d) {
    if (d.children) {
      d._children = d.children
      d.children = null
    } else {
      d.children = d._children
      d._children = null
    }
    this.update(d)
  }
}
