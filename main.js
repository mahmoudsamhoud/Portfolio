// Remove the details link event listeners
document.querySelectorAll(".details-link").forEach((link) => {
  link.addEventListener("click", (e) => {
    e.preventDefault();
    const projectId = link.getAttribute("data-project");
    const modal = document.getElementById(projectId);
    if (modal) {
      modal.style.display = "block";
    }
  });
});
