function toggleSidebar() {
  document.getElementById("sidebar").classList.toggle("active");
}

/* ===== REVENUE CHART ===== */
new Chart(document.getElementById("revenueChart"), {
  type: "line",
  data: {
    labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    datasets: [{
      label: "Revenue ($)",
      data: [2000, 3500, 4200, 6100, 8000, 12450],
      borderColor: "#38bdf8",
      backgroundColor: "rgba(56,189,248,0.2)",
      tension: 0.4
    }]
  }
});

/* ===== USER GROWTH ===== */
new Chart(document.getElementById("userChart"), {
  type: "bar",
  data: {
    labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    datasets: [{
      label: "Users",
      data: [200, 400, 600, 900, 1200, 1540],
      backgroundColor: "#22c55e"
    }]
  }
});

/* ===== PRODUCT STATUS ===== */
new Chart(document.getElementById("productChart"), {
  type: "doughnut",
  data: {
    labels: ["Approved", "Pending", "Rejected"],
    datasets: [{
      data: [70, 20, 10],
      backgroundColor: ["#22c55e", "#f59e0b", "#ef4444"]
    }]
  }
});