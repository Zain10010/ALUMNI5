document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('alumniForm');

    // Add input event listeners to remove error class when user starts typing
    const inputs = form.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            this.classList.remove('error');
        });
    });

    // Form validation
    form.addEventListener('submit', function(e) {
        // Remove any existing error classes
        inputs.forEach(input => input.classList.remove('error'));

        // Validate required fields
        const requiredFields = form.querySelectorAll('[required]');
        let isValid = true;

        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                isValid = false;
                field.classList.add('error');
            }
        });

        if (!isValid) {
            e.preventDefault();
            // Show error message
            showAlert('Please fill in all required fields.', 'error');
            return;
        }

        // Form is valid, let it submit
        showAlert('Submitting registration...', 'success');
    });

    // Function to show alerts
    function showAlert(message, type) {
        // Remove existing alerts
        const existingAlert = document.querySelector('.alert');
        if (existingAlert) {
            existingAlert.remove();
        }

        // Create new alert
        const alert = document.createElement('div');
        alert.className = `alert alert-${type}`;
        alert.textContent = message;

        // Insert alert before the form
        form.parentNode.insertBefore(alert, form);

        // Auto-remove alert after 5 seconds
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 5000);
    }

    // Add visual feedback for form interactions
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentNode.classList.add('focused');
        });

        input.addEventListener('blur', function() {
            this.parentNode.classList.remove('focused');
        });
    });
});

