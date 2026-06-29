(function () {
  var stored = null;

  try {
    stored = localStorage.getItem("portfolio-theme");
  } catch (error) {
    stored = null;
  }

  document.documentElement.setAttribute(
    "data-theme",
    stored === "dark" || stored === "light" ? stored : "light"
  );
})();
