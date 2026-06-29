// EduAakashaa – Frontend JS

document.addEventListener('DOMContentLoaded', () => {
  // Collapsible nav toggle (all screen sizes)
  const hamburger = document.getElementById('hamburger');
  const nav = document.getElementById('nav');

  if (hamburger && nav) {
    const closeNav = () => {
      nav.classList.remove('open');
      hamburger.classList.remove('active');
    };

    hamburger.addEventListener('click', (e) => {
      e.stopPropagation();
      nav.classList.toggle('open');
      hamburger.classList.toggle('active');
    });

    // Close after picking a destination (but let dropdown parents expand)
    nav.querySelectorAll('.nav__link').forEach(link => {
      link.addEventListener('click', () => {
        if (!link.closest('.nav__item--dropdown')) closeNav();
      });
    });

    // Close when clicking outside the menu
    document.addEventListener('click', (e) => {
      if (nav.classList.contains('open') &&
          !nav.contains(e.target) && !hamburger.contains(e.target)) {
        closeNav();
      }
    });

    // Close on Escape
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closeNav();
    });
  }

  // Grouped dropdown toggles. The top-level item is a category (href="#"), so
  // never navigate on click. Below 1024px the nav is a panel and the dropdown
  // is an accordion toggled by tap; above that it opens on hover (CSS).
  const dropdownItems = document.querySelectorAll('.nav__item--dropdown');
  dropdownItems.forEach(item => {
    const link = item.querySelector('.nav__link');
    if (link) {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        if (window.innerWidth <= 1024) {
          // accordion: only one section open at a time
          dropdownItems.forEach(o => { if (o !== item) o.classList.remove('open'); });
          item.classList.toggle('open');
        }
      });
    }
  });

  // Sidebar active link highlight on scroll
  const sidebar = document.getElementById('sidebar');
  if (sidebar) {
    const sidebarLinks = sidebar.querySelectorAll('.sidebar__link');
    const sections = [];

    sidebarLinks.forEach(link => {
      const href = link.getAttribute('href');
      if (href && href.startsWith('#')) {
        const target = document.querySelector(href);
        if (target) sections.push({ el: target, link });
      }
    });

    const updateActive = () => {
      const scrollY = window.scrollY + 200;
      let current = null;

      sections.forEach(({ el, link }) => {
        if (el.offsetTop <= scrollY) {
          current = link;
        }
      });

      sidebarLinks.forEach(l => l.classList.remove('active'));
      if (current) current.classList.add('active');
    };

    window.addEventListener('scroll', updateActive, { passive: true });
    updateActive();
  }

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      const target = document.querySelector(anchor.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // Sticky header shadow on scroll
  const header = document.getElementById('header');
  if (header) {
    window.addEventListener('scroll', () => {
      header.style.boxShadow = window.scrollY > 50
        ? '0 2px 12px rgba(0,0,0,0.08)'
        : 'none';
    }, { passive: true });
  }
});
