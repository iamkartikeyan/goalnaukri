/**
 * Goal Naukri Main Interactive JS
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Mobile Menu Toggle
    const menuToggle = document.querySelector('.menu-toggle');
    const siteNavigation = document.getElementById('site-navigation') || document.querySelector('.main-navigation');
    
    if (menuToggle && siteNavigation) {
        menuToggle.addEventListener('click', (e) => {
            e.preventDefault();
            const isExpanded = menuToggle.getAttribute('aria-expanded') === 'true';
            menuToggle.setAttribute('aria-expanded', !isExpanded);
            siteNavigation.classList.toggle('toggled');
        });
    }

    // 2. Back to Top Button
    let backToTop = document.querySelector('.generate-back-to-top');
    if (!backToTop) {
        backToTop = document.createElement('a');
        backToTop.href = '#';
        backToTop.className = 'generate-back-to-top';
        backToTop.setAttribute('aria-label', 'Scroll to top');
        backToTop.innerHTML = `
            <svg viewBox="0 0 320 512" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor">
                <path d="M177 159.7l136 136c9.4 9.4 9.4 24.6 0 33.9l-22.6 22.6c-9.4 9.4-24.6 9.4-33.9 0L160 255.9l-96.5 96.4c-9.4 9.4-24.6 9.4-33.9 0L7 329.7c-9.4-9.4-9.4-24.6 0-33.9l136-136c9.4-9.5 24.6-9.5 34-.1z"/>
            </svg>
        `;
        backToTop.style.position = 'fixed';
        backToTop.style.bottom = '30px';
        backToTop.style.right = '30px';
        backToTop.style.width = '42px';
        backToTop.style.height = '42px';
        backToTop.style.display = 'flex';
        backToTop.style.alignItems = 'center';
        backToTop.style.justifyContent = 'center';
        backToTop.style.borderRadius = '4px';
        backToTop.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
        backToTop.style.color = '#ffffff';
        backToTop.style.zIndex = '9999';
        backToTop.style.opacity = '0';
        backToTop.style.visibility = 'hidden';
        backToTop.style.transition = 'opacity 0.3s ease, visibility 0.3s ease, background-color 0.3s ease';
        backToTop.style.textDecoration = 'none';
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

    backToTop.addEventListener('click', (e) => {
        e.preventDefault();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // 3. Search Bar Interaction
    const searchInputs = document.querySelectorAll('input[type="search"]');
    searchInputs.forEach(input => {
        const form = input.closest('form');
        if (form) {
            form.addEventListener('submit', (e) => {
                const query = input.value.trim();
                if (query) {
                    // Search in articles on page or filter
                    const articles = document.querySelectorAll('article, .gb-container-fd6fcffb');
                    if (articles.length > 0) {
                        e.preventDefault();
                        let foundCount = 0;
                        articles.forEach(art => {
                            const text = art.textContent.toLowerCase();
                            if (text.includes(query.toLowerCase())) {
                                art.style.display = '';
                                foundCount++;
                            } else {
                                art.style.display = 'none';
                            }
                        });
                        
                        let searchNotice = document.getElementById('search-notice');
                        if (!searchNotice) {
                            searchNotice = document.createElement('div');
                            searchNotice.id = 'search-notice';
                            searchNotice.style.padding = '15px';
                            searchNotice.style.marginBottom = '20px';
                            searchNotice.style.backgroundColor = '#e7f5fe';
                            searchNotice.style.border = '1px solid #83b0de';
                            searchNotice.style.borderRadius = '4px';
                            searchNotice.style.color = '#2f4468';
                            const main = document.querySelector('main') || document.querySelector('#content');
                            if (main) main.insertBefore(searchNotice, main.firstChild);
                        }
                        if (searchNotice) {
                            searchNotice.innerHTML = `Showing results for: <strong>"${query}"</strong> (${foundCount} found) - <a href="#" id="clear-search" style="color: #1b78e2; text-decoration: underline;">Clear filter</a>`;
                            document.getElementById('clear-search')?.addEventListener('click', (ce) => {
                                ce.preventDefault();
                                articles.forEach(art => art.style.display = '');
                                searchNotice.remove();
                                input.value = '';
                            });
                        }
                    }
                }
            });
        }
    });

    // 4. Contact Form Handling
    const contactForm = document.querySelector('.wpforms-form') || document.querySelector('form[action*="contact"]');
    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const submitBtn = contactForm.querySelector('button[type="submit"]');
            if (submitBtn) {
                const originalText = submitBtn.innerHTML;
                submitBtn.disabled = true;
                submitBtn.innerHTML = 'Sending...';
                setTimeout(() => {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalText;
                    
                    const confirmation = document.createElement('div');
                    confirmation.className = 'wpforms-confirmation-container-full';
                    confirmation.style.padding = '20px';
                    confirmation.style.backgroundColor = '#e9fbe5';
                    confirmation.style.border = '1px solid #7bdcb5';
                    confirmation.style.borderRadius = '4px';
                    confirmation.style.marginTop = '20px';
                    confirmation.style.color = '#006633';
                    confirmation.innerHTML = '<strong>धन्यवाद!</strong> आपका संदेश सफलतापूर्वक भेज दिया गया है। हम जल्द ही आपसे संपर्क करेंगे।';
                    
                    contactForm.reset();
                    contactForm.parentNode.insertBefore(confirmation, contactForm.nextSibling);
                    setTimeout(() => confirmation.remove(), 6000);
                }, 800);
            }
        });
    }

    // 5. Subscription Form Handling
    const subForms = document.querySelectorAll('.reach-form-inline');
    subForms.forEach(sf => {
        sf.addEventListener('submit', (e) => {
            e.preventDefault();
            const input = sf.querySelector('input[type="email"]');
            if (input && input.value) {
                alert(`Thank you for subscribing with ${input.value}! You will receive the latest job updates.`);
                input.value = '';
            }
        });
    });
});
