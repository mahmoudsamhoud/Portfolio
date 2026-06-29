/**
 * Template Name: MyResume
 * Template URL: https://bootstrapmade.com/free-html-bootstrap-template-my-resume/
 * Updated: Jun 29 2024 with Bootstrap v5.3.3
 * Author: BootstrapMade.com
 * License: https://bootstrapmade.com/license/
 */

(function () {
  "use strict";

  const themeStorageKey = "portfolio-theme";
  const docEl = document.documentElement;

  function getStoredTheme() {
    try {
      return localStorage.getItem(themeStorageKey);
    } catch (error) {
      return null;
    }
  }

  function storeTheme(theme) {
    try {
      localStorage.setItem(themeStorageKey, theme);
    } catch (error) {
      // The theme still changes for this visit if storage is unavailable.
    }
  }

  function getPreferredTheme() {
    const storedTheme = getStoredTheme();

    if (storedTheme === "light" || storedTheme === "dark") {
      return storedTheme;
    }

    return "light";
  }

  function updateThemeButtons(theme) {
    const nextTheme = theme === "dark" ? "light" : "dark";
    const label = `Switch to ${nextTheme} theme`;

    document
      .querySelectorAll("[data-theme-toggle], .theme-toggle-btn, .theme-toggle-fixed")
      .forEach((button) => {
        button.setAttribute("aria-label", label);
        button.setAttribute("title", label);

        const text = button.querySelector(".theme-toggle-label");
        if (text) {
          text.textContent = nextTheme === "dark" ? "Dark" : "Light";
        }
      });
  }

  function setTheme(theme, shouldStore) {
    docEl.setAttribute("data-theme", theme);
    docEl.style.colorScheme = theme;

    if (shouldStore) {
      storeTheme(theme);
    }

    updateThemeButtons(theme);
  }

  function createThemeButton() {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "theme-toggle-fixed";
    button.setAttribute("data-theme-toggle", "");
    button.innerHTML =
      '<i class="bi bi-sun icon-light" aria-hidden="true"></i>' +
      '<i class="bi bi-moon-stars icon-dark" aria-hidden="true"></i>';

    return button;
  }

  function initThemeToggle() {
    if (!document.querySelector("[data-theme-toggle], .theme-toggle-fixed")) {
      document.body.appendChild(createThemeButton());
    }

    setTheme(getPreferredTheme(), false);

    document
      .querySelectorAll("[data-theme-toggle], .theme-toggle-btn, .theme-toggle-fixed")
      .forEach((button) => {
        button.addEventListener("click", () => {
          const currentTheme = docEl.getAttribute("data-theme") === "dark" ? "dark" : "light";
          setTheme(currentTheme === "dark" ? "light" : "dark", true);
        });
      });

  }

  initThemeToggle();

  /**
   * Header toggle
   */
  const headerToggleBtn = document.querySelector(".header-toggle");

  function headerToggle() {
    const header = document.querySelector("#header");
    if (!header || !headerToggleBtn) return;

    header.classList.toggle("header-show");
    headerToggleBtn.classList.toggle("bi-list");
    headerToggleBtn.classList.toggle("bi-x");
  }

  if (headerToggleBtn) {
    headerToggleBtn.addEventListener("click", headerToggle);
  }

  /**
   * Hide mobile nav on same-page/hash links
   */
  document.querySelectorAll("#navmenu a").forEach((navmenu) => {
    navmenu.addEventListener("click", () => {
      if (document.querySelector(".header-show")) {
        headerToggle();
      }
    });
  });

  /**
   * Toggle mobile nav dropdowns
   */
  document.querySelectorAll(".navmenu .toggle-dropdown").forEach((navmenu) => {
    navmenu.addEventListener("click", function (e) {
      e.preventDefault();
      this.parentNode.classList.toggle("active");
      this.parentNode.nextElementSibling.classList.toggle("dropdown-active");
      e.stopImmediatePropagation();
    });
  });

  /**
   * Preloader
   */
  const preloader = document.querySelector("#preloader");
  if (preloader) {
    window.addEventListener("load", () => {
      preloader.remove();
    });
  }

  /**
   * Scroll top button
   */
  const scrollTop = document.querySelector(".scroll-top");

  function toggleScrollTop() {
    if (!scrollTop) return;

    window.scrollY > 100
      ? scrollTop.classList.add("active")
      : scrollTop.classList.remove("active");
  }

  if (scrollTop) {
    scrollTop.addEventListener("click", (e) => {
      e.preventDefault();
      window.scrollTo({
        top: 0,
        behavior: "smooth",
      });
    });
  }

  window.addEventListener("load", toggleScrollTop);
  document.addEventListener("scroll", toggleScrollTop);

  /**
   * Animation on scroll function and init
   */
  function aosInit() {
    if (!window.AOS) return;

    AOS.init({
      duration: 600,
      easing: "ease-in-out",
      once: true,
      mirror: false,
    });
  }
  window.addEventListener("load", aosInit);

  /**
   * Init typed.js
   */
  const selectTyped = document.querySelector(".typed");
  if (selectTyped && window.Typed) {
    const typedStrings = selectTyped.getAttribute("data-typed-items");

    if (typedStrings) {
      new Typed(".typed", {
        strings: typedStrings.split(",").map((item) => item.trim()),
        loop: true,
        typeSpeed: 100,
        backSpeed: 50,
        backDelay: 2000,
      });
    }
  }

  /**
   * Initiate Pure Counter
   */
  if (window.PureCounter) {
    new PureCounter();
  }

  /**
   * Animate the skills items on reveal
   */
  if (window.Waypoint) {
    document.querySelectorAll(".skills-animation").forEach((item) => {
      new Waypoint({
        element: item,
        offset: "80%",
        handler: function () {
          item.querySelectorAll(".progress .progress-bar").forEach((el) => {
            el.style.width = el.getAttribute("aria-valuenow") + "%";
          });
        },
      });
    });
  }

  /**
   * Initiate glightbox
   */
  if (window.GLightbox) {
    GLightbox({
      selector: ".glightbox",
    });
  }

  /**
   * Init isotope layout and filters
   */
  if (window.imagesLoaded && window.Isotope) {
    document.querySelectorAll(".isotope-layout").forEach(function (isotopeItem) {
      const layout = isotopeItem.getAttribute("data-layout") ?? "masonry";
      const filter = isotopeItem.getAttribute("data-default-filter") ?? "*";
      const sort = isotopeItem.getAttribute("data-sort") ?? "original-order";

      let initIsotope;
      imagesLoaded(isotopeItem.querySelector(".isotope-container"), function () {
        initIsotope = new Isotope(isotopeItem.querySelector(".isotope-container"), {
          itemSelector: ".isotope-item",
          layoutMode: layout,
          filter: filter,
          sortBy: sort,
        });
      });

      isotopeItem
        .querySelectorAll(".isotope-filters li")
        .forEach(function (filters) {
          filters.addEventListener(
            "click",
            function () {
              const activeFilter = isotopeItem.querySelector(
                ".isotope-filters .filter-active"
              );

              if (activeFilter) {
                activeFilter.classList.remove("filter-active");
              }

              this.classList.add("filter-active");

              if (initIsotope) {
                initIsotope.arrange({
                  filter: this.getAttribute("data-filter"),
                });
              }

              aosInit();
            },
            false
          );
        });
    });
  }

  /**
   * Init swiper sliders
   */
  function initSwiper() {
    if (!window.Swiper) return;

    document.querySelectorAll(".init-swiper").forEach(function (swiperElement) {
      const configElement = swiperElement.querySelector(".swiper-config");
      if (!configElement) return;

      const config = JSON.parse(configElement.innerHTML.trim());

      if (
        swiperElement.classList.contains("swiper-tab") &&
        typeof window.initSwiperWithCustomPagination === "function"
      ) {
        window.initSwiperWithCustomPagination(swiperElement, config);
      } else {
        new Swiper(swiperElement, config);
      }
    });
  }

  window.addEventListener("load", initSwiper);

  /**
   * Correct scrolling position upon page load for URLs containing hash links.
   */
  window.addEventListener("load", function () {
    if (!window.location.hash) return;

    const section = document.querySelector(window.location.hash);
    if (!section) return;

    setTimeout(() => {
      const scrollMarginTop = getComputedStyle(section).scrollMarginTop;
      window.scrollTo({
        top: section.offsetTop - parseInt(scrollMarginTop, 10),
        behavior: "smooth",
      });
    }, 100);
  });

  /**
   * Navmenu Scrollspy
   */
  const navmenulinks = document.querySelectorAll(".navmenu a");

  function navmenuScrollspy() {
    navmenulinks.forEach((navmenulink) => {
      if (!navmenulink.hash) return;

      const section = document.querySelector(navmenulink.hash);
      if (!section) return;

      const position = window.scrollY + 200;
      if (
        position >= section.offsetTop &&
        position <= section.offsetTop + section.offsetHeight
      ) {
        document
          .querySelectorAll(".navmenu a.active")
          .forEach((link) => link.classList.remove("active"));
        navmenulink.classList.add("active");
      } else {
        navmenulink.classList.remove("active");
      }
    });
  }
  window.addEventListener("load", navmenuScrollspy);
  document.addEventListener("scroll", navmenuScrollspy);

  // Project Modals
  document.addEventListener("DOMContentLoaded", function () {
    const modalTriggers = document.querySelectorAll(
      ".preview-link, .details-link"
    );
    const modals = document.querySelectorAll(".modal");
    const closeButtons = document.querySelectorAll(".close-modal");

    function openModal(modalId) {
      const modal = document.getElementById(modalId);
      if (modal) {
        modal.style.display = "block";
        document.body.style.overflow = "hidden";
      }
    }

    function closeModal(modal) {
      if (!modal) return;

      modal.style.display = "none";
      document.body.style.overflow = "";
    }

    modalTriggers.forEach((trigger) => {
      trigger.addEventListener("click", function (e) {
        const projectId = this.getAttribute("data-project");
        if (!projectId) return;

        e.preventDefault();
        openModal(projectId);
      });
    });

    closeButtons.forEach((button) => {
      button.addEventListener("click", function () {
        closeModal(this.closest(".modal"));
      });
    });

    modals.forEach((modal) => {
      modal.addEventListener("click", function (e) {
        if (e.target === this) {
          closeModal(this);
        }
      });
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") {
        modals.forEach((modal) => {
          if (modal.style.display === "block") {
            closeModal(modal);
          }
        });
      }
    });
  });

  // Reading Progress Bar
  function initReadingProgress() {
    const progressBar = document.querySelector(".reading-progress-bar");
    if (!progressBar) return;

    function updateProgress() {
      const windowHeight = window.innerHeight;
      const documentHeight =
        document.documentElement.scrollHeight - windowHeight;
      const scrolled = window.scrollY;
      const progress = documentHeight > 0 ? (scrolled / documentHeight) * 100 : 0;
      progressBar.style.width = `${progress}%`;
    }

    window.addEventListener("scroll", updateProgress);
    window.addEventListener("resize", updateProgress);
    updateProgress();
  }

  document.addEventListener("DOMContentLoaded", initReadingProgress);

  // Skills section filters
  document.addEventListener("DOMContentLoaded", function () {
    const filterButtons = document.querySelectorAll(".skill-filter");
    const filterableTools = document.querySelectorAll(".filterable-tool");
    const categoryGroups = document.querySelectorAll(".skills-category-group");

    if (!filterButtons.length || !filterableTools.length) return;

    function applySkillsFilter(selectedFilter) {
      filterableTools.forEach((tool) => {
        const categories =
          tool
            .getAttribute("data-categories")
            ?.split(",")
            .map((cat) => cat.trim()) || [];
        const matches =
          selectedFilter === "all" || categories.includes(selectedFilter);
        tool.classList.toggle("is-hidden", !matches);
      });

      categoryGroups.forEach((group) => {
        const visibleTools = group.querySelectorAll(
          ".filterable-tool:not(.is-hidden)"
        );
        group.classList.toggle("is-hidden", visibleTools.length === 0);
      });
    }

    filterButtons.forEach((button) => {
      button.addEventListener("click", () => {
        filterButtons.forEach((btn) => btn.classList.remove("active"));
        button.classList.add("active");
        applySkillsFilter(button.getAttribute("data-filter"));
      });
    });

    applySkillsFilter("all");
  });
})();
