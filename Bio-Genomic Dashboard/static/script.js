/**
 * PhyloShield Frontend JavaScript
 * ===============================
 *
 * This module handles the client-side interactivity for the DNA analysis platform.
 * It manages user input, API communication, and real-time data visualization.
 *
 * Features:
 * - Sequence input validation
 * - Asynchronous API calls to Flask backend
 * - Chart.js integration for GC content visualization
 * - Responsive UI updates with loading states
 * - Error handling and user feedback
 *
 * Dependencies: Chart.js, Fetch API
 */

// Global variables for chart management
let gcChart = null;

/**
 * Initialize the application when DOM is loaded
 */
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    initializeChart();
});

/**
 * Set up event listeners for user interactions
 */
function initializeEventListeners() {
    const analyzeBtn = document.getElementById('analyze-btn');

    // Analyze button click handler
    analyzeBtn.addEventListener('click', handleAnalysis);

    // Enter key support for text areas
    document.getElementById('human-sequence').addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && e.ctrlKey) {
            handleAnalysis();
        }
    });

    document.getElementById('animal-sequence').addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && e.ctrlKey) {
            handleAnalysis();
        }
    });
}

/**
 * Initialize the GC content comparison chart
 */
function initializeChart() {
    const ctx = document.getElementById('gc-chart').getContext('2d');

    gcChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Human', 'Animal'],
            datasets: [{
                label: 'GC Content (%)',
                data: [0, 0],
                backgroundColor: [
                    'rgba(0, 255, 136, 0.8)',  // Neon green
                    'rgba(0, 34, 68, 0.8)'     // Deep sea blue
                ],
                borderColor: [
                    'rgba(0, 255, 136, 1)',
                    'rgba(0, 34, 68, 1)'
                ],
                borderWidth: 2,
                borderRadius: 8,
                borderSkipped: false,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 18, 34, 0.9)',
                    titleColor: '#00ff88',
                    bodyColor: '#ffffff',
                    borderColor: 'rgba(0, 255, 136, 0.5)',
                    borderWidth: 1,
                    cornerRadius: 8,
                    displayColors: false,
                    callbacks: {
                        label: function(context) {
                            return `GC Content: ${context.parsed.y.toFixed(1)}%`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    grid: {
                        color: 'rgba(0, 255, 136, 0.1)'
                    },
                    ticks: {
                        color: '#cccccc',
                        callback: function(value) {
                            return value + '%';
                        }
                    }
                },
                x: {
                    grid: {
                        color: 'rgba(0, 255, 136, 0.1)'
                    },
                    ticks: {
                        color: '#cccccc'
                    }
                }
            },
            animation: {
                duration: 1000,
                easing: 'easeOutQuart'
            }
        }
    });
}

/**
 * Handle the sequence analysis process
 */
async function handleAnalysis() {
    const analyzeBtn = document.getElementById('analyze-btn');
    const humanSeq = document.getElementById('human-sequence').value.trim();
    const animalSeq = document.getElementById('animal-sequence').value.trim();
    const gasLevel = parseFloat(document.getElementById('gas-level').value) || 0;

    // Input validation
    if (!humanSeq || !animalSeq) {
        showError('Please enter both human and animal DNA sequences.');
        return;
    }

    if (humanSeq.length < 10 || animalSeq.length < 10) {
        showError('DNA sequences must be at least 10 nucleotides long.');
        return;
    }

    // Update UI for loading state
    setLoadingState(true);

    try {
        // Send analysis request to backend
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                human_sequence: humanSeq,
                animal_sequence: animalSeq,
                gas_level: gasLevel
            })
        });

        const result = await response.json();

        if (result.success) {
            displayResults(result.data);
        } else {
            showError(result.error || 'Analysis failed. Please try again.');
        }

    } catch (error) {
        console.error('Analysis error:', error);
        showError('Network error. Please check your connection and try again.');
    } finally {
        setLoadingState(false);
    }
}

/**
 * Display analysis results in the UI
 * @param {Object} data - Analysis results from the backend
 */
function displayResults(data) {
    const resultsSection = document.getElementById('results-section');

    // Update sequence identity
    document.getElementById('identity-value').textContent = data.sequence_identity.toFixed(1);
    document.getElementById('identity-category').textContent = data.comparison_summary.identity_category;

    // Update GC content values
    document.getElementById('human-gc').textContent = data.human_gc_content.toFixed(1);
    document.getElementById('animal-gc').textContent = data.animal_gc_content.toFixed(1);

    // Update chart
    updateChart(data.human_gc_content, data.animal_gc_content);

    // Update health risk
    document.getElementById('mutation-rate').textContent = data.health_risk.predicted_mutation_rate.toFixed(3);
    const riskLevelElement = document.getElementById('risk-level');
    riskLevelElement.textContent = data.health_risk.risk_level;
    riskLevelElement.setAttribute('data-level', data.health_risk.risk_level);

    // Update comparison summary
    document.getElementById('gc-difference').textContent = data.comparison_summary.gc_difference.toFixed(1);
    document.getElementById('relationship').textContent = data.comparison_summary.identity_category.split(' ')[0];

    // Show results section
    resultsSection.classList.remove('hidden');
}

/**
 * Update the GC content chart with new data
 * @param {number} humanGC - Human GC content percentage
 * @param {number} animalGC - Animal GC content percentage
 */
function updateChart(humanGC, animalGC) {
    if (gcChart) {
        gcChart.data.datasets[0].data = [humanGC, animalGC];
        gcChart.update();
    }
}

/**
 * Set loading state for the analyze button
 * @param {boolean} loading - Whether to show loading state
 */
function setLoadingState(loading) {
    const analyzeBtn = document.getElementById('analyze-btn');

    if (loading) {
        analyzeBtn.disabled = true;
        analyzeBtn.textContent = '🔬 Analyzing...';
        analyzeBtn.classList.add('loading');
    } else {
        analyzeBtn.disabled = false;
        analyzeBtn.textContent = '🔬 Analyze Sequences';
        analyzeBtn.classList.remove('loading');
    }
}

/**
 * Display error message to the user
 * @param {string} message - Error message to display
 */
function showError(message) {
    // Create error notification
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-notification';
    errorDiv.innerHTML = `
        <div class="error-content">
            <span class="error-icon">⚠️</span>
            <span class="error-message">${message}</span>
            <button class="error-close">&times;</button>
        </div>
    `;

    // Add error styles
    errorDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: rgba(255, 0, 0, 0.9);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 0, 0, 0.5);
        border-radius: 12px;
        padding: 16px;
        z-index: 1000;
        box-shadow: 0 8px 32px rgba(255, 0, 0, 0.3);
        animation: slideIn 0.3s ease-out;
    `;

    // Close button functionality
    errorDiv.querySelector('.error-close').addEventListener('click', function() {
        errorDiv.remove();
    });

    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (errorDiv.parentNode) {
            errorDiv.remove();
        }
    }, 5000);

    document.body.appendChild(errorDiv);
}

/**
 * Utility function to validate DNA sequence format
 * @param {string} sequence - DNA sequence to validate
 * @returns {boolean} - True if valid
 */
function validateDNASequence(sequence) {
    const validChars = /^[ATGC\s]+$/i;
    return validChars.test(sequence) && sequence.replace(/\s/g, '').length >= 10;
}

/**
 * Add CSS animation for error notifications
 */
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    .error-notification {
        font-family: 'JetBrains Mono', monospace;
    }

    .error-content {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .error-icon {
        font-size: 20px;
    }

    .error-message {
        color: white;
        font-weight: 500;
    }

    .error-close {
        background: none;
        border: none;
        color: white;
        font-size: 24px;
        cursor: pointer;
        padding: 0;
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .error-close:hover {
        color: #ccc;
    }
`;
document.head.appendChild(style);