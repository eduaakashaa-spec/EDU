// EduAakashaa – Frontend JS

document.addEventListener('DOMContentLoaded', () => {
  // Mobile hamburger toggle
  const hamburger = document.getElementById('hamburger');
  const nav = document.getElementById('nav');

  if (hamburger && nav) {
    hamburger.addEventListener('click', () => {
      nav.classList.toggle('open');
      hamburger.classList.toggle('active');
    });
  }

  // Mobile dropdown toggles
  const dropdownItems = document.querySelectorAll('.nav__item--dropdown');
  dropdownItems.forEach(item => {
    const link = item.querySelector('.nav__link');
    if (link) {
      link.addEventListener('click', (e) => {
        if (window.innerWidth <= 768) {
          e.preventDefault();
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
