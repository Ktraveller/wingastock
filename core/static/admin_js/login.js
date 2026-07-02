function loginUser(event) {
  event.preventDefault();

  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const error = document.getElementById("error");

  // SIMPLE DEMO LOGIN (replace later with backend)
  if (email === "admin@winga.com" && password === "1234") {
    alert("Login successful!");
    window.location.href = "admin-dashboard.html";
  } else {
    error.textContent = "Invalid email or password";
  }

  return false;
}