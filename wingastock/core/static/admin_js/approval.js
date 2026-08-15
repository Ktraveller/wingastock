function toggleSidebar() {
  document.getElementById("sidebar").classList.toggle("active");
}

// SEARCH APPROVALS
function searchApprovals() {
  let input = document.getElementById("searchInput").value.toLowerCase();
  let rows = document.querySelectorAll("#approvalTable tr");

  rows.forEach(row => {
    row.style.display = row.textContent.toLowerCase().includes(input)
      ? ""
      : "none";
  });
}

// APPROVE PRODUCT
function approveProduct(btn) {
  let row = btn.parentElement.parentElement;

  row.cells[5].innerHTML = '<span class="active">Approved</span>';
}

// REJECT PRODUCT
function rejectProduct(btn) {
  let row = btn.parentElement.parentElement;

  row.cells[5].innerHTML = '<span class="pending" style="background:#ef4444;">Rejected</span>';
}