function toggleSidebar() {
  document.getElementById("sidebar").classList.toggle("active");
}

// SEARCH PRODUCTS
function searchProducts() {
  let input = document.getElementById("searchInput").value.toLowerCase();
  let rows = document.querySelectorAll("#productTable tr");

  rows.forEach(row => {
    row.style.display = row.textContent.toLowerCase().includes(input)
      ? ""
      : "none";
  });
}

// DELETE PRODUCT
function deleteProduct(btn) {
  btn.parentElement.parentElement.remove();
}

// EDIT PRODUCT
function editProduct(btn) {
  let row = btn.parentElement.parentElement;

  let name = prompt("Edit Product Name:", row.cells[1].innerText);
  let seller = prompt("Edit Seller:", row.cells[2].innerText);
  let price = prompt("Edit Price:", row.cells[3].innerText);

  if (name) row.cells[1].innerText = name;
  if (seller) row.cells[2].innerText = seller;
  if (price) row.cells[3].innerText = price;
}

// ADD PRODUCT (demo only)
function addProduct() {
  let table = document.getElementById("productTable");

  let id = Math.floor(Math.random() * 1000);
  let name = prompt("Product Name:");
  let seller = prompt("Seller Name:");
  let price = prompt("Price:");

  if (!name || !seller || !price) return;

  let row = `
    <tr>
      <td>${id}</td>
      <td>${name}</td>
      <td>${seller}</td>
      <td>$${price}</td>
      <td><span class="pending">Pending</span></td>
      <td>
        <button class="btn edit" onclick="editProduct(this)">Edit</button>
        <button class="btn delete" onclick="deleteProduct(this)">Delete</button>
      </td>
    </tr>
  `;

  table.innerHTML += row;
}