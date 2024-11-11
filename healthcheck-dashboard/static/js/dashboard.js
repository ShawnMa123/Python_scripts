document.addEventListener('DOMContentLoaded', function() {
    function updateDashboard() {
        fetch('/api/health')
            .then(response => response.json())
            .then(data => {
                let servicesTable = document.getElementById('services');
                // Clear existing rows, keeping the header
                while(servicesTable.rows.length > 1) {
                    servicesTable.deleteRow(-1);
                }
                for (const [service, status] of Object.entries(data)) {
                    let row = servicesTable.insertRow();
                    let cellService = row.insertCell(0);
                    let cellStatus = row.insertCell(1);
                    let cellTime = row.insertCell(2);

                    cellService.textContent = service;
                    cellStatus.innerHTML = `<span class="${status.status === 'HEALTHY' ? 'healthy' : 'unhealthy'}">${status.status}</span>`;
                    cellTime.textContent = new Date().toLocaleString(); // This will show the time when the dashboard was last updated
                }
            });
    }

    // Update dashboard every 15 seconds
    setInterval(updateDashboard, 15000);
    updateDashboard(); // Initial update
});
