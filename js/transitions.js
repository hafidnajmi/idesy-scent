/**
 * Indoeasy Scent — Smooth Page Transition & Responsive Navigation
 * Keeps Navbar stable & frozen while <main> content smoothly fades in / fades out.
 * Provides touch-friendly, highly sensitive dropdown toggles on mobile, tablet & desktop.
 * 100% compatible with native HTML page layouts, Tailwind, and scripts.
 */
(function () {
    'use strict';

    // Fade in main content on page load
    function initPageFadeIn() {
        var main = document.querySelector('main');
        if (!main) return;

        // Apply initial hidden state before frame render
        main.style.opacity = '0';
        main.style.transform = 'translateY(12px)';
        main.style.transition = 'none';

        requestAnimationFrame(function () {
            requestAnimationFrame(function () {
                main.style.transition = 'opacity 0.35s cubic-bezier(0.25, 0.46, 0.45, 0.94), transform 0.35s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
                main.style.opacity = '1';
                main.style.transform = 'translateY(0)';
            });
        });
    }

    // Intercept internal links for smooth fade out before page navigation
    function attachLinkTransitions() {
        document.addEventListener('click', function (e) {
            var link = e.target.closest('a[href]');
            if (!link) return;

            // If this is a parent dropdown trigger link, let dropdown toggle handle it
            var parentGroup = link.closest('.relative.group');
            if (parentGroup) {
                var dropdown = parentGroup.querySelector('.nav-dropdown');
                if (dropdown && link === parentGroup.querySelector('.nav-link')) {
                    // Check if it's a mobile/touch tap intending to toggle dropdown
                    if (!dropdown.classList.contains('dropdown-open')) {
                        return; // Do not navigate! Dropdown click handler will open it
                    }
                }
            }

            var href = link.getAttribute('href');
            if (!href) return;

            // Ignore external, mailto, tel, javascript, new tabs, or anchor-only links
            if (href.indexOf('http') === 0 || href.indexOf('//') === 0 ||
                href.indexOf('mailto') === 0 || href.indexOf('tel') === 0 ||
                href.indexOf('javascript') === 0 || link.target === '_blank') return;

            // Handle hash anchors on the same page
            if (href.charAt(0) === '#') return;

            var currentFile = window.location.pathname.split('/').pop() || 'index.html';
            var targetFile  = href.split('#')[0].split('/').pop() || 'index.html';
            var targetHash  = href.indexOf('#') > -1 ? href.split('#')[1] : null;

            // Same page anchor click
            if (currentFile === targetFile && targetHash) return;

            // Fade out <main> before navigating
            e.preventDefault();
            var main = document.querySelector('main');
            if (main) {
                main.style.transition = 'opacity 0.2s cubic-bezier(0.4, 0, 1, 1), transform 0.25s cubic-bezier(0.4, 0, 1, 1)';
                main.style.opacity = '0';
                main.style.transform = 'translateY(-8px)';
            }

            setTimeout(function () {
                window.location.href = href;
            }, 200);
        });
    }

    // Desktop & Tablet Navbar Dropdowns (Touch & Click Support)
    function initDesktopDropdowns() {
        var dropdownGroups = document.querySelectorAll('.relative.group');

        dropdownGroups.forEach(function (group) {
            var triggerLink = group.querySelector('.nav-link');
            var dropdownMenu = group.querySelector('.nav-dropdown');

            if (!triggerLink || !dropdownMenu) return;

            triggerLink.addEventListener('click', function (e) {
                var isOpen = dropdownMenu.classList.contains('dropdown-open');

                if (!isOpen) {
                    // First click / tap: Open dropdown and prevent navigating away
                    e.preventDefault();
                    e.stopPropagation();

                    // Close any other open desktop dropdowns first
                    document.querySelectorAll('.nav-dropdown.dropdown-open').forEach(function (d) {
                        d.classList.remove('dropdown-open');
                        var parentLink = d.parentElement.querySelector('.nav-link');
                        if (parentLink) parentLink.classList.remove('dropdown-open');
                    });

                    // Open this dropdown
                    dropdownMenu.classList.add('dropdown-open');
                    triggerLink.classList.add('dropdown-open');
                } else {
                    // Second click / tap: Toggle close if tapped again
                    e.preventDefault();
                    e.stopPropagation();
                    dropdownMenu.classList.remove('dropdown-open');
                    triggerLink.classList.remove('dropdown-open');
                }
            });
        });

        // Close dropdown when tapping anywhere outside
        document.addEventListener('click', function (e) {
            if (!e.target.closest('.relative.group')) {
                document.querySelectorAll('.nav-dropdown.dropdown-open').forEach(function (d) {
                    d.classList.remove('dropdown-open');
                    var parentLink = d.parentElement.querySelector('.nav-link');
                    if (parentLink) parentLink.classList.remove('dropdown-open');
                });
            }
        });
    }

    // Mobile Drawer Navigation System (Ultra-Sensitive & Touch-Optimized)
    function initMobileDrawer() {
        var menuBtn = document.getElementById('mobile-menu-btn');
        var drawer = document.getElementById('mobile-drawer');
        var panel = document.getElementById('mobile-drawer-panel');
        var closeBtn = document.getElementById('mobile-drawer-close');

        if (!menuBtn || !drawer || !panel) return;

        function openDrawer(e) {
            if (e) {
                e.preventDefault();
                e.stopPropagation();
            }
            drawer.classList.remove('opacity-0', 'pointer-events-none');
            drawer.classList.add('opacity-100');
            panel.classList.remove('translate-x-full');
            panel.classList.add('translate-x-0');
            document.body.style.overflow = 'hidden';
        }

        function closeDrawer(e) {
            if (e) {
                e.preventDefault();
                e.stopPropagation();
            }
            drawer.classList.remove('opacity-100');
            drawer.classList.add('opacity-0', 'pointer-events-none');
            panel.classList.remove('translate-x-0');
            panel.classList.add('translate-x-full');
            document.body.style.overflow = '';
        }

        menuBtn.addEventListener('click', openDrawer);
        if (closeBtn) closeBtn.addEventListener('click', closeDrawer);

        drawer.addEventListener('click', function (e) {
            if (e.target === drawer) closeDrawer(e);
        });

        // Mobile Accordion Toggle for TENTANG KAMI, PRODUK, AREA LAYANAN
        var accordionBtns = drawer.querySelectorAll('.mobile-accordion-btn');
        accordionBtns.forEach(function (btn) {
            btn.addEventListener('click', function (e) {
                e.preventDefault();
                e.stopPropagation();

                var content = this.nextElementSibling;
                var icon = this.querySelector('.material-symbols-outlined');
                if (!content) return;

                var isHidden = content.classList.contains('hidden');
                if (isHidden) {
                    content.classList.remove('hidden');
                    if (icon) {
                        icon.style.transform = 'rotate(180deg)';
                    }
                } else {
                    content.classList.add('hidden');
                    if (icon) {
                        icon.style.transform = 'rotate(0deg)';
                    }
                }
            });
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function () {
            initPageFadeIn();
            attachLinkTransitions();
            initDesktopDropdowns();
            initMobileDrawer();
        });
    } else {
        initPageFadeIn();
        attachLinkTransitions();
        initDesktopDropdowns();
        initMobileDrawer();
    }
})();
