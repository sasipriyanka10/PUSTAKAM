document.addEventListener('DOMContentLoaded', () => {
    // Scroll Reveal Observer
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.15
    };

    const scrollObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                // Optional: Stop observing once revealed
                // observer.unobserve(entry.target); 
            }
        });
    }, observerOptions);

    // Select elements that SHOULD be animated
    const animatedElements = document.querySelectorAll(
        '.animate-fade-up, .section-title, .book-card, .category-card, .about-card, .info-item'
    );

    animatedElements.forEach((el, index) => {
        el.classList.add('animate-ready'); // Add class to indicate JS is processing
        // Stagger animations
        el.style.transitionDelay = `${index % 5 * 0.1}s`;
        scrollObserver.observe(el);
    });

    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 20) {
                navbar.classList.add('scrolled');
                navbar.style.background = 'rgba(255, 255, 255, 0.95)';
                navbar.style.boxShadow = '0 12px 40px rgba(0,0,0,0.1)';
            } else {
                navbar.classList.remove('scrolled');
                navbar.style.background = 'rgba(255, 255, 255, 0.85)';
                navbar.style.boxShadow = '0 8px 32px rgba(0, 0, 0, 0.05)';
            }
        });
    }

    // Button ripple effect
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(btn => {
        btn.addEventListener('click', function (e) {
            let x = e.clientX - e.target.getBoundingClientRect().left;
            let y = e.clientY - e.target.getBoundingClientRect().top;
            let ripples = document.createElement('span');
            ripples.style.left = x + 'px';
            ripples.style.top = y + 'px';
            this.appendChild(ripples);
            setTimeout(() => {
                ripples.remove()
            }, 1000);
        });
    });
});

// Determine visibility via CSS class
const styleSheet = document.createElement("style");
styleSheet.innerText = `
    /* Only hide if JS is active and adding the class */
    .animate-ready {
        opacity: 0;
        transform: translateY(30px);
        transition: opacity 0.6s cubic-bezier(0.2, 0.8, 0.2, 1), transform 0.6s cubic-bezier(0.2, 0.8, 0.2, 1);
    }
    
    .animate-ready.visible {
        opacity: 1 !important;
        transform: translateY(0) !important;
    }
    
    /* Ripple Effect */
    .btn { position: relative; overflow: hidden; }
    .btn span {
        position: absolute;
        background: rgba(255, 255, 255, 0.5);
        transform: translate(-50%, -50%);
        pointer-events: none;
        border-radius: 50%;
        animation: ripple 0.6s linear infinite;
    }
    @keyframes ripple {
        0% { width: 0px; height: 0px; opacity: 0.5; }
        100% { width: 500px; height: 500px; opacity: 0; }
    }
`;
document.head.appendChild(styleSheet);
