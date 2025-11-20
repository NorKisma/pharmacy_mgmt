
    document.addEventListener("DOMContentLoaded", function () {
      const sidebar = document.getElementById('sidebar');
      const mainContent = document.getElementById('main-content');
      const toggleBtn = document.getElementById('sidebarToggle');
      const navbarToggle = document.getElementById('navbarSidebarToggle');
      const overlay = document.getElementById('overlay');

      function toggleSidebar() {
        if (window.innerWidth <= 768) {
          sidebar.classList.toggle('open');
          overlay.classList.toggle('active');
        } else {
          sidebar.classList.toggle('collapsed');
          mainContent.classList.toggle('expanded');
        }
      }

      if (toggleBtn) toggleBtn.addEventListener('click', toggleSidebar);
      if (navbarToggle) navbarToggle.addEventListener('click', toggleSidebar);

      if (overlay) {
        overlay.addEventListener('click', () => {
          sidebar.classList.remove('open');
          overlay.classList.remove('active');
        });
      }
    });

 
 
   document.addEventListener("DOMContentLoaded", function () {
  const toggleBtn = document.getElementById("themeToggle");
  const themeIcon = document.getElementById("themeIcon");
  const navbar = document.getElementById("mainNavbar");

  // Load saved theme
  const savedTheme = localStorage.getItem("theme") || "light";
  applyTheme(savedTheme);

  // Toggle theme on click
  toggleBtn.addEventListener("click", () => {
    const newTheme = document.body.classList.toggle("dark-mode") ? "dark" : "light";
    localStorage.setItem("theme", newTheme);
    applyTheme(newTheme);
  });

  function applyTheme(theme) {
    if (theme === "dark") {
      themeIcon.classList.replace("fa-moon", "fa-sun");
      navbar.classList.add("navbar-dark", "bg-dark");
      navbar.classList.remove("navbar-custom", "text-white");
      toggleBtn.classList.replace("btn-outline-light", "btn-outline-secondary"); // Dark mode
    } else {
      themeIcon.classList.replace("fa-sun", "fa-moon");
      navbar.classList.remove("bg-dark", "navbar-dark");
      navbar.classList.add("navbar-custom", "text-white");
      toggleBtn.classList.replace("btn-outline-secondary", "btn-outline-light"); // Light mode
    }
  }
});
