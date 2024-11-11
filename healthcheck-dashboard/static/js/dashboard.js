document.addEventListener('DOMContentLoaded', function() {
    function updateDashboard() {
        fetch('/api/health')
            .then(response => response.json())
            .then(data => {
                let servicesDiv = document.getElementById('services');
                servicesDiv.innerHTML = '';
                for (const [service, status] of Object.entries(data)) {
                    let statusDiv = document.createElement('div');
                    statusDiv.textContent = `${service}: ${status.status}`;
                    statusDiv.className = status.status === 'HEALTHY' ? 'healthy' : 'unhealthy';
                    servicesDiv.appendChild(statusDiv);
                }
            });
    }

    // Update dashboard every 15 seconds
    setInterval(updateDashboard, 15000);
    updateDashboard(); // Initial update
});
