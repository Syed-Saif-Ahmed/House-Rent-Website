document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.getElementById('contact-form');

    contactForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission

        const formData = new FormData(contactForm); // Get form data

        fetch('/submit_contact_form', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                // Success: Redirect to thank you page or handle response as needed
                window.location.href = '/thank_you';
            } else {
                // Error: Handle error response
                console.error('Error submitting form:', response.statusText);
                alert('An error occurred while submitting the form. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error submitting form:', error);
            alert('An error occurred while submitting the form. Please try again.');
        });
    });
});
