// Custom navbar toggle for mobile menu
document.addEventListener('DOMContentLoaded', () => {

  // Get all "navbar-burger" elements
  const navbarBurgers = document.querySelectorAll('.navbar-burger');

  // Add a click event on each navbar burger
  navbarBurgers.forEach(burger => {
    burger.addEventListener('click', () => {

      // Get the target from the "data-target" attribute
      const target = burger.dataset.target;
      const menu = document.getElementById(target);

      // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
      burger.classList.toggle('is-active');
      if (menu) {
        menu.classList.toggle('is-active');
      }

    });
  });

  // Close mobile menu when clicking on a menu item (optional enhancement)
  const navbarItems = document.querySelectorAll('.navbar-item');
  navbarItems.forEach(item => {
    item.addEventListener('click', () => {
      // Close mobile menu when an item is clicked
      const burger = document.querySelector('.navbar-burger');
      const menu = document.querySelector('.navbar-menu');
      
      if (burger && menu && window.innerWidth <= 768) {
        burger.classList.remove('is-active');
        menu.classList.remove('is-active');
      }
    });
  });

});
