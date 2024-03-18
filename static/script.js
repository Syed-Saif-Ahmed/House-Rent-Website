document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('form');

    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission

        // Get the form data
        const formData = new FormData(form);

        // Send the form data to the Flask server
        fetch('/submit_contact_form', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                // Optionally, redirect the user to a thank you page
                window.location.href = '/thank_you';
            } else {
                console.error('Error:', response.statusText);
                // Optionally, handle errors or display an error message
            }
        })
        .catch(error => {
            console.error('Error:', error);
            // Optionally, handle errors or display an error message
        });
    });
});
