// dashboard.js
document.addEventListener("DOMContentLoaded", () => {
    /* ===== Monthly Revenue Chart ===== */
    const revenueCtx = document.getElementById("revenueChart");
    if (revenueCtx) {
        new Chart(revenueCtx, {
            type: "line",
            data: {
                labels: revenue_labels || [],
                datasets: [{
                    label: "Revenue",
                    data: revenue_values || [],
                    borderColor: "rgba(54,162,235,1)",
                    backgroundColor: "rgba(54,162,235,0.2)",
                    tension: 0.3,
                    fill: true
                }]
            },
            options: { responsive:true, plugins:{legend:{display:true, position:'top'}} }
        });
    }

    /* ===== Sales Chart ===== */
    const salesCtx = document.getElementById("salesChart");
    if (salesCtx) {
        new Chart(salesCtx, {
            type: "bar",
            data: {
                labels: sales_labels || [],
                datasets: [{
                    label: "Sales",
                    data: sales_values || [],
                    backgroundColor: "rgba(255,99,132,0.7)"
                }]
            },
            options: { responsive:true, plugins:{legend:{display:true, position:'top'}} }
        });
    }

    /* ===== DataTables for Invoices ===== */
    const invoicesTable = $("#invoicesTable").DataTable({ order:[[2,'desc']], pageLength:10 });

    /* ===== Invoice Filtering by Status ===== */
    const filterButtons = document.querySelectorAll(".summary-card");
    filterButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            const filter = btn.getAttribute("data-filter");
            invoicesTable.rows().every(function() {
                const status = $(this.node()).data("status");
                if(filter === "all" || status === filter){ $(this.node()).show(); }
                else { $(this.node()).hide(); }
            });
        });
    });

    /* ===== Card Hover Effect ===== */
    document.querySelectorAll(".dash-card").forEach(card => {
        card.addEventListener("mouseenter", ()=>card.style.transform="translateY(-5px)");
        card.addEventListener("mouseleave", ()=>card.style.transform="translateY(0)");
    });
});
