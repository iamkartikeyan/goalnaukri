/**
 * Goal Naukri - Clean Interactive Mobile & Desktop Script
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Mobile Menu Toggle
    const menuToggle = document.querySelector('.menu-toggle');
    const siteNav = document.getElementById('site-navigation') || document.querySelector('.main-navigation');
    
    if (menuToggle && siteNav) {
        const toggleMenu = (e) => {
            if (e) {
                e.preventDefault();
                e.stopPropagation();
            }
            const isExpanded = menuToggle.getAttribute('aria-expanded') === 'true';
            menuToggle.setAttribute('aria-expanded', !isExpanded);
            siteNav.classList.toggle('toggled');
        };

        menuToggle.addEventListener('click', toggleMenu);

        // Close menu when tapping outside
        document.addEventListener('click', (e) => {
            if (siteNav.classList.contains('toggled') && !siteNav.contains(e.target) && !menuToggle.contains(e.target)) {
                siteNav.classList.remove('toggled');
                menuToggle.setAttribute('aria-expanded', 'false');
            }
        });
    }

    // 2. Back to Top Button
    let backToTop = document.querySelector('.generate-back-to-top');
    if (!backToTop) {
        backToTop = document.createElement('button');
        backToTop.className = 'generate-back-to-top';
        backToTop.setAttribute('aria-label', 'Scroll to top');
        backToTop.innerHTML = '<i class="fa-solid fa-arrow-up"></i>';
        backToTop.style.position = 'fixed';
        backToTop.style.bottom = '25px';
        backToTop.style.right = '20px';
        backToTop.style.width = '42px';
        backToTop.style.height = '42px';
        backToTop.style.display = 'flex';
        backToTop.style.alignItems = 'center';
        backToTop.style.justifyContent = 'center';
        backToTop.style.borderRadius = '50%';
        backToTop.style.backgroundColor = '#1e59be';
        backToTop.style.color = '#ffffff';
        backToTop.style.border = 'none';
        backToTop.style.cursor = 'pointer';
        backToTop.style.zIndex = '9999';
        backToTop.style.opacity = '0';
        backToTop.style.visibility = 'hidden';
        backToTop.style.transition = 'opacity 0.3s ease, visibility 0.3s ease, transform 0.2s ease';
        backToTop.style.boxShadow = '0 4px 14px rgba(0,0,0,0.3)';
        document.body.appendChild(backToTop);
    }

    window.addEventListener('scroll', () => {
        if (window.scrollY > 300) {
            backToTop.style.opacity = '1';
            backToTop.style.visibility = 'visible';
        } else {
            backToTop.style.opacity = '0';
            backToTop.style.visibility = 'hidden';
        }
    });

    backToTop.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // 3. Search Filter Handling
    const searchForms = document.querySelectorAll('.gn-search-form, form[role="search"], .wp-block-search');
    searchForms.forEach(form => {
        form.addEventListener('submit', (e) => {
            const input = form.querySelector('input[type="search"], input[type="text"]');
            if (input && input.value.trim()) {
                const query = input.value.trim().toLowerCase();
                const cards = document.querySelectorAll('.gn-post-card, article.post');
                if (cards.length > 0) {
                    e.preventDefault();
                    let count = 0;
                    cards.forEach(card => {
                        if (card.textContent.toLowerCase().includes(query)) {
                            card.style.display = 'flex';
                            count++;
                        } else {
                            card.style.display = 'none';
                        }
                    });

                    let notice = document.getElementById('search-notice');
                    if (!notice) {
                        notice = document.createElement('div');
                        notice.id = 'search-notice';
                        notice.style.padding = '14px 18px';
                        notice.style.marginBottom = '20px';
                        notice.style.backgroundColor = '#e7f5fe';
                        notice.style.border = '1px solid #83b0de';
                        notice.style.borderRadius = '8px';
                        notice.style.color = '#2f4468';
                        notice.style.fontSize = '14px';
                        const container = document.querySelector('.gn-posts-list') || document.querySelector('.gn-content-area');
                        if (container) container.insertBefore(notice, container.firstChild);
                    }
                    if (notice) {
                        notice.innerHTML = `Showing results for: <strong>"${query}"</strong> (${count} found) - <a href="#" id="clear-search" style="color:#1b78e2; font-weight:600; text-decoration:underline;">Clear filter</a>`;
                        document.getElementById('clear-search')?.addEventListener('click', (ce) => {
                            ce.preventDefault();
                            cards.forEach(c => c.style.display = 'flex');
                            notice.remove();
                            input.value = '';
                        });
                    }
                }
            }
        });
    });

    // 4. Contact Form Handling
    const contactForm = document.querySelector('.gn-contact-form') || document.querySelector('.wpforms-form');
    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const btn = contactForm.querySelector('button[type="submit"], input[type="submit"]');
            if (btn) {
                const orig = btn.innerHTML || btn.value;
                if (btn.tagName === 'INPUT') btn.value = 'भेजा जा रहा है...';
                else btn.innerHTML = 'भेजा जा रहा है...';
                btn.disabled = true;

                setTimeout(() => {
                    btn.disabled = false;
                    if (btn.tagName === 'INPUT') btn.value = orig;
                    else btn.innerHTML = orig;

                    const msg = document.createElement('div');
                    msg.style.padding = '16px 20px';
                    msg.style.backgroundColor = '#e9fbe5';
                    msg.style.border = '1px solid #7bdcb5';
                    msg.style.borderRadius = '8px';
                    msg.style.marginTop = '20px';
                    msg.style.color = '#006633';
                    msg.style.fontSize = '15px';
                    msg.innerHTML = '<strong>धन्यवाद!</strong> आपका संदेश सफलतापूर्वक भेज दिया गया है। हम जल्द ही आपसे संपर्क करेंगे।';

                    contactForm.reset();
                    contactForm.parentNode.insertBefore(msg, contactForm.nextSibling);
                    setTimeout(() => msg.remove(), 6000);
                }, 800);
            }
        });
    }

    // 5. Subscription Form Handling
    const subForms = document.querySelectorAll('.gn-sub-form, .reach-form-inline');
    subForms.forEach(sf => {
        sf.addEventListener('submit', (e) => {
            e.preventDefault();
            const input = sf.querySelector('input[type="email"]');
            if (input && input.value) {
                alert(`Thank you for subscribing with ${input.value}! You will receive latest job updates.`);
                input.value = '';
            }
        });
    });
});
