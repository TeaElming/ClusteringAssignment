/** @format */

class DropDownOptions extends HTMLElement {
  constructor() {
    super()
    this.attachShadow({ mode: "open" })

    this.shadowRoot.innerHTML = `
      <form id="options-form">
        <label for="method-select">Select Method:</label>
        <select id="method-select" disabled>
          <option value="" disabled selected>--Select Clustering Method--</option>
          <option value="kmeans">K-means</option>
          <option value="kmeansopt">K-means Optimised</option>
          <option value="hierchical">Hierarchical</option>
        </select>
      </form>
    `

    this.methodSelect = this.shadowRoot.querySelector("#method-select")
  }

  connectedCallback() {
    // Enable the dropdown once the component is fully loaded
    this.methodSelect.disabled = false
  }
}

customElements.define("drop-down-options", DropDownOptions)
