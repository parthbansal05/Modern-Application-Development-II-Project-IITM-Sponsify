window.addEventListener("resize", updateLayout);

function updateLayout() {
  const col = document.querySelector(".col-lg-5");
  if (col) {
    if (window.innerWidth <= 768) {
      // Adjust the breakpoint as needed
      col.classList.add("col-md-6");
      col.classList.remove("col-lg-5");
    } else {
      col.classList.add("col-lg-5");
      col.classList.remove("col-md-6");
    }
  }
}

// Call the function initially to set the initial layout
updateLayout();
