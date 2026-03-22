// Basic routing and interactions
document.addEventListener('DOMContentLoaded', function() {
    // Card click navigation
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('click', function() {
            const link = this.getAttribute('data-link');
            if (link) {
                window.location.href = link;
            }
        });
    });

    // Load dynamic content for pages
    if (document.getElementById('air-status')) {
        fetch('/api/air_quality')
            .then(response => response.json())
            .then(data => {
                document.getElementById('air-status').textContent = `Status: ${data.status} - ${data.suggestion}`;
            })
            .catch(error => console.error('Error fetching air quality:', error));
    }

    if (document.getElementById('food-tip')) {
        fetch('/api/food_tips')
            .then(response => response.json())
            .then(data => {
                document.getElementById('food-tip').textContent = `${data.item}: ${data.tip}`;
            })
            .catch(error => console.error('Error fetching food tips:', error));
    }

    if (document.getElementById('body-state')) {
        fetch('/api/circadian_rhythm')
            .then(response => response.json())
            .then(data => {
                document.getElementById('body-state').textContent = `At ${data.time}: ${data.bio_state}`;
            })
            .catch(error => console.error('Error fetching circadian data:', error));
    }
});