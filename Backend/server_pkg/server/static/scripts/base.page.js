window.onload = function () {
  sidebar.style.left = "-250px";
};

// JavaScript function to toggle the sidebar visibility
function toggleSidebar() {
  const sidebar = document.getElementById("sidebar");
  const sidebarToggle = document.getElementById("sidebarToggle");

  if (sidebar.style.left === "-250px") {
    sidebar.style.left = "0";
    sidebarToggle.innerHTML = '<span class="fas fa-times"> </span>';
  } else {
    sidebar.style.left = "-250px";
    sidebarToggle.innerHTML = '<span class="fas fa-bars"> </span>';
  }
}
