document.addEventListener('DOMContentLoaded', function() {
    var sendButtons = document.querySelectorAll('.send-reply');

    sendButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var modalId = button.getAttribute('data-target');
            var modal = document.querySelector(modalId);
            var replyMessage = modal.querySelector('.form-control').value;
            var name = button.getAttribute('data-name');
            var email = button.getAttribute('data-email');

            // Send the message to the server
            sendMessage(name, email, replyMessage);

            // Close the modal
            $(modalId).modal('hide');

            // Clear the reply message textarea
            modal.querySelector('.form-control').value = '';
        });
    });

    function sendMessage(name, email, message) {
        // Make an AJAX request to send the message to the Flask server
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/send_message', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onload = function() {
            if (xhr.status === 200) {
                console.log('Message sent successfully');
            } else {
                console.error('Error sending message:', xhr.statusText);
            }
        };
        xhr.onerror = function() {
            console.error('Error sending message:', xhr.statusText);
        };
        xhr.send(JSON.stringify({ name: name, email: email, message: message }));
    }
});

document.getElementById("logoutBtn").addEventListener("click", function() {
    // Perform logout actions here
    // For example, redirect to logout endpoint or clear session
    window.location.href = "/admin_logout";
});