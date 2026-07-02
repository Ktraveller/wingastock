function toggleSidebar() {
  document.getElementById("sidebar").classList.toggle("active");
}

/* ===== LINE CHART ===== */
const lineCtx = document.getElementById("lineChart");

new Chart(lineCtx, {
  type: "line",
  data: {
    labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    datasets: [{
      label: "Users",
      data: [200, 400, 600, 900, 1200, 1540],
      borderColor: "#38bdf8",
      backgroundColor: "rgba(56,189,248,0.2)",
      tension: 0.4
    }]
  }
});

/* ===== BAR CHART ===== */
const barCtx = document.getElementById("barChart");

new Chart(barCtx, {
  type: "bar",
  data: {
    labels: ["Electronics", "Fashion", "Food", "Books", "Other"],
    datasets: [{
      label: "Sales",
      data: [300, 500, 200, 400, 150],
      backgroundColor: "#38bdf8"
    }]
  }
});

/* ===== DOUGHNUT CHART ===== */
const doughnutCtx = document.getElementById("doughnutChart");

new Chart(doughnutCtx, {
  type: "doughnut",
  data: {
    labels: ["Buyers", "Sellers", "Admins"],
    datasets: [{
      data: [70, 25, 5],
      backgroundColor: ["#38bdf8", "#22c55e", "#f59e0b"]
    }]
  }
});