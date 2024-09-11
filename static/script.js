document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('upload-form');
    const notification = document.getElementById('notification');
    const uploadUrl = form.getAttribute('data-upload-url');

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(form);
        fetch(uploadUrl, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            showNotification(data.message);
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('An error occurred while uploading the file.');
        });
    });

    function showNotification(message) {
        notification.textContent = message;
        notification.classList.add('show');
        setTimeout(() => {
            notification.classList.remove('show');
        }, 4000); // Hide after 4 seconds
    }
});
