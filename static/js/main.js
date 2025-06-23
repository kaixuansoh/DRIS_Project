// Main JavaScript file for DRIS

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });
    
    // Handle alert dismissal - Auto-dismiss alerts after 5 seconds
    var alertList = document.querySelectorAll('.alert.alert-dismissible:not(.alert-permanent)');
    alertList.forEach(function (alert) {
        setTimeout(function() {
            if (alert && document.body.contains(alert)) {
                // Use Bootstrap's alert dismiss functionality if available
                if (typeof bootstrap !== 'undefined') {
                    var bsAlert = new bootstrap.Alert(alert);
                    bsAlert.close();
                } else {
                    // Fallback to manual removal
                    alert.style.opacity = '0';
                    setTimeout(function() {
                        alert.remove();
                    }, 150);
                }
            }
        }, 5000); // 5 seconds
    });
    
    // Shelter management form validation
    const shelterForm = document.querySelector('form#shelter-form');
    if (shelterForm) {
        shelterForm.addEventListener('submit', function(e) {
            const totalCapacity = parseInt(document.getElementById('id_total_capacity').value);
            const currentOccupancy = parseInt(document.getElementById('id_current_occupancy').value);
            
            if (currentOccupancy > totalCapacity) {
                e.preventDefault();
                alert('Error: Current occupancy cannot exceed total capacity.');
                return false;
            }
        });
    }
    
    // Handle form validation
    var forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
});
