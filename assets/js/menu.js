/* Menú del sidebar: hamburguesa en móvil y desplegables.
   Equivale a lo que hacía el JS del tema Cele, sin jQuery. */
(function () {
  'use strict';

  var toggle = document.querySelector('.toggle-navigation');
  var menuContainer = document.querySelector('.menu-primary-container');
  var sidebarContainer = document.querySelector('.sidebar-primary-container');

  if (toggle && menuContainer) {
    toggle.addEventListener('click', function () {
      var open = menuContainer.classList.toggle('open');
      toggle.classList.toggle('open', open);
      toggle.setAttribute('aria-expanded', String(open));
      if (sidebarContainer) sidebarContainer.classList.toggle('open', open);
    });
  }

  document.querySelectorAll('.toggle-dropdown').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var item = btn.closest('.menu-item-has-children');
      var open = item.classList.toggle('open');
      btn.setAttribute('aria-expanded', String(open));
    });
  });

  // El submenú de la página activa se abre solo.
  var current = document.querySelector('.menu-primary-items .current-menu-item');
  if (current) {
    var parent = current.closest('.menu-item-has-children');
    if (parent) {
      parent.classList.add('open');
      var b = parent.querySelector(':scope > .toggle-dropdown');
      if (b) b.setAttribute('aria-expanded', 'true');
    }
  }
})();
