/**
 * Indoeasy Scent — Smooth Page Transition
 * Keeps Navbar stable & frozen while <main> content smoothly fades in / fades out.
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

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function () {
            initPageFadeIn();
            attachLinkTransitions();
        });
    } else {
        initPageFadeIn();
        attachLinkTransitions();
    }
})();
