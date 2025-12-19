document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(event) {
            event.preventDefault();
            document.getElementById('form-container').setAttribute("style", "display: none !important;");
            document.getElementById('success-message').setAttribute("style", "display: block !important;");
        });
    }
});