function toggleSidebar() {
  document.getElementById("sidebar").classList.toggle("active");
}

// SEARCH USERS
function searchUsers() {
  let input = document.getElementById("searchInput").value.toLowerCase();
  let rows = document.querySelectorAll("#usersTable tr");

  rows.forEach(row => {
    row.style.display = row.textContent.toLowerCase().includes(input)
      ? ""
      : "none";
  });
}

// DELETE USER
function deleteUser(btn) {
  btn.parentElement.parentElement.remove();
}

// EDIT USER
function editUser(btn) {
  let row = btn.parentElement.parentElement;

  let name = prompt("Edit Name:", row.cells[1].innerText);
  let email = prompt("Edit Email:", row.cells[2].innerText);

  if (name) row.cells[1].innerText = name;
  if (email) row.cells[2].innerText = email;
}