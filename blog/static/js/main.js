const navSlide = () => {
    const burger = document.querySelector('.burger');
    const nav = document.querySelector('.nav-links');
    const navLinks = document.querySelectorAll('.nav-links li');

    burger.addEventListener('click', () => {
        // Toggle Nav
        nav.classList.toggle('nav-active');

        // Animate Links
        navLinks.forEach((link, index) => {
            if (link.style.animation) {
                link.style.animation = '';
            } else {
                link.style.animation = `navLinkFade 0.5s ease forwards ${index / 7 + 0.3}s`;
            }
        });

        // Burger Animation
        burger.classList.toggle('toggle');
    });
}

const smoothScroll = () => {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
}

const handleSubscription = () => {
    const form = document.getElementById('subscription-form');
    const message = document.getElementById('subscription-message');

    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            const formData = new FormData(form);

            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
                .then(response => response.json())
                .then(data => {
                    message.textContent = data.message;
                    if (data.success) {
                        message.style.color = 'green';
                        form.reset();
                    } else {
                        message.style.color = 'red';
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    message.textContent = 'An error occurred. Please try again.';
                    message.style.color = 'red';
                });
        });
    }
}

const app = () => {
    navSlide();
    smoothScroll();
    handleSubscription();
}

document.addEventListener('DOMContentLoaded', () => {
    app();
});
