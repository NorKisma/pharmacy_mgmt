document.addEventListener("DOMContentLoaded", function() {
    console.log("Pharmacy System Loaded ✅");

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
       2. INITIALIZE DATA TABLES (if any)
       Optional: Add later if needed
    ======================================= */
    if ($.fn.DataTable) {
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
    } else {
        console.warn("DataTables library not loaded.");
    }
});

/* =======================================
   3. TOAST FUNCTION
======================================= */
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toastContainer');
    if (!toastContainer) return;

    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-bg-${type} border-0 mb-2`;
    toast.role = 'alert';
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');

    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>`;

    toastContainer.appendChild(toast);

    const bsToast = new bootstrap.Toast(toast, { delay: 5000 });
    bsToast.show();

    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}

/* =======================================
   4. CONFIRM DELETE MODAL
   Usage: confirmDelete(id, name, formSelector)
======================================= */
function confirmDelete(id, name, formSelector) {
    const modalElement = document.getElementById('deleteModal');
    if (!modalElement) return;

    const modal = new bootstrap.Modal(modalElement);
    document.getElementById('deleteItemName').textContent = name;

    const form = document.querySelector(formSelector);
    if (form && form.dataset.baseAction) {
        form.action = form.dataset.baseAction.replace('ID', id);
    }

    modal.show();
}

