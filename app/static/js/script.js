document.addEventListener("DOMContentLoaded", function() {
    console.log("Pharmacy System Loaded ✅");

    /* =======================================
       HELPER FUNCTION: TOAST NOTIFICATIONS
       (Unified from both snippets)
    ======================================= */
    /**
     * Shows a Bootstrap Toast notification.
     * @param {string} message - The message to display.
     * @param {string} type - The toast background type (info, success, danger, etc.).
     */
    function showToast(message, type = 'info') {
        const toastContainer = document.getElementById('toastContainer');
        if (!toastContainer) return;

        const bgClass = type === 'error' ? 'danger' : type;
        
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-bg-${bgClass} border-0 mb-2`;
        toast.role = 'alert';
        toast.setAttribute('aria-live', 'assertive');
        toast.setAttribute('aria-atomic', 'true');

        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>`;

        toastContainer.appendChild(toast);

        // Using a 4-second delay for consistency
        const bsToast = new bootstrap.Toast(toast, { delay: 4000 }); 
        bsToast.show();

        toast.addEventListener('hidden.bs.toast', () => {
            toast.remove();
        });
    }

    /* =======================================
       1. FORM VALIDATION (Bootstrap)
    ======================================= */
    const forms = document.querySelectorAll('form.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                showToast("Please fill all required fields!", "danger");
            }
            form.classList.add('was-validated');
        });
    });

    /* =======================================
       2. INITIALIZE DATA TABLES 
    ======================================= */
    // Standard DataTable Initialization (for .datatable class)
    if (typeof $ !== 'undefined' && $.fn.DataTable) {
        $('.datatable').DataTable({
            pageLength: 10,
            lengthMenu: [5, 10, 25, 50, 100],
            ordering: true,
            responsive: true,
            autoWidth: false,
            searching: true,
            language: {
                search: "🔍 Search:",
                lengthMenu: "Show _MENU_ entries per page",
                paginate: { previous: "&laquo;", next: "&raquo;" },
                info: "Showing _START_ to _END_ of _TOTAL_ entries"
            }
        });

        // Specific DataTable for #userTable (assuming server-side pagination)
        $('#userTable').DataTable({
            "paging": false, 
            "info": false,
            "searching": false, 
            "columnDefs": [{ "orderable": false, "targets": 4 }], // Disable ordering on action column
        });
    } else {
        console.warn("DataTables library not loaded.");
    }
    
    /* =======================================
       3. PROCESS SERVER-SIDE FLASH MESSAGES
    ======================================= */
    const flashDiv = document.getElementById('flash-messages');
    if(flashDiv){
        Array.from(flashDiv.children).forEach(div => {
            showToast(div.dataset.message, div.dataset.category);
        });
    }

    /* =======================================
       4. CONFIRM DELETE MODAL LOGIC (AJAX)
    ======================================= */
    let deleteUrl = null; 
    let deleteRowId = null;
    
    const deleteModalElement = document.getElementById('deleteModal');
    if (!deleteModalElement) return;

    const deleteModal = new bootstrap.Modal(deleteModalElement);

    // Get CSRF Token (NOTE: This variable uses Jinja syntax and MUST be set in your template)
    const csrfToken = "{{ csrf_token() }}"; 

    // Unified helper for legacy confirmDelete function (if needed)
    window.confirmDelete = function(id, name, formSelector) {
        const form = document.querySelector(formSelector);
        if (form && form.dataset.baseAction) {
             // Assuming ID is passed in the URL for form submission
            form.action = form.dataset.baseAction.replace('ID', id); 
        }
        document.getElementById('deleteItemName').textContent = name; // Assuming this ID exists for general confirmation
        deleteModal.show();
    }


    // Event delegation for AJAX delete buttons (class .delete-btn)
    document.body.addEventListener('click', function(e) {
        if(e.target.closest('.delete-btn')) {
            const btn = e.target.closest('.delete-btn');
            // Assuming data attributes for user deletion
            deleteRowId = btn.dataset.userId; 
            deleteUrl = btn.dataset.deleteUrl; 
            const name = btn.dataset.userName;
            
            document.getElementById('deleteItemName').textContent = name; // Update modal text
            deleteModal.show();
        }
    });

    // Confirm Delete Action (AJAX POST)
    document.getElementById('confirmDeleteBtn').addEventListener('click', function() {
        if(!deleteUrl) {
            showToast('Delete URL not set.', 'danger');
            deleteModal.hide();
            return;
        }

        fetch(deleteUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // Include CSRF token for security
                'X-CSRFToken': csrfToken 
            }
        })
        .then(response => {
            if (!response.ok) {
                // Read JSON error body or throw general error
                return response.json().catch(() => {
                    throw new Error(`HTTP error! status: ${response.status}`);
                });
            }
            return response.json();
        })
        .then(data => {
            if(data.status === 'success'){
                // Remove the table row from the DOM
                const row = document.getElementById(`user-${deleteRowId}`);
                if(row) row.remove();
                showToast(data.message, 'success');
            } else {
                // Show server-side error message
                showToast(data.message || 'Deletion failed due to a server issue.', 'danger');
            }
        })
        .catch(error => {
            console.error('Fetch Error:', error);
            showToast('An unexpected error occurred while deleting.', 'danger');
        })
        .finally(() => {
            deleteModal.hide();
        });
    });

    // Make the unified showToast function globally available if other modules need it
    window.showToast = showToast;
});