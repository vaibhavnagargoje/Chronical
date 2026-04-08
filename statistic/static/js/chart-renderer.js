/**
 * Renders dynamic charts based on data fetched from the API.
 * Uses Chart.js for rendering.
 */

document.addEventListener('DOMContentLoaded', function() {
    const chartContainers = document.querySelectorAll('.dynamic-chart-container');
    
    // Make sure Chart.js is loaded
    if (typeof Chart === 'undefined') {
        console.error('Chart.js is not loaded. Dynamic charts cannot be rendered.');
        return;
    }

    // Set some default Chart.js defaults
    Chart.defaults.font.family = "'Lato', 'Inter', 'Roboto', sans-serif";
    Chart.defaults.color = '#333';

    chartContainers.forEach(container => {
        initChart(container);
    });
});

function initChart(container) {
    const templateSlug = container.getAttribute('data-template-slug');
    const district = container.getAttribute('data-district');
    
    if (!templateSlug || !district) {
        console.error('Missing data-template-slug or data-district on chart container', container);
        return;
    }

    // Store the chart instance on the container so we can destroy it when updating
    container._chartInstance = null;
    
    fetchAndRenderChart(container, templateSlug, district, null, null);
}

function fetchAndRenderChart(container, templateSlug, district, filter1Value, filter2Value) {
    // Show loading
    const loadingHtml = `
        <div class="loading-indicator text-center text-gray-500 py-10">
            <i class="fas fa-spinner fa-spin fa-2x mb-2"></i>
            <p>Loading chart data...</p>
        </div>
    `;
    
    // Only show loading if we haven't rendered yet
    if (!container._chartInstance && !container.querySelector('canvas')) {
        container.innerHTML = loadingHtml;
    } else if (container.querySelector('.loading-indicator')) {
        container.querySelector('.loading-indicator').style.display = 'block';
        if (container.querySelector('canvas')) {
            container.querySelector('canvas').style.opacity = '0.5';
        }
    }

    let url = `/api/chart-data/${templateSlug}/?district=${encodeURIComponent(district)}`;
    if (filter1Value) {
        url += `&filter1=${encodeURIComponent(filter1Value)}`;
    }
    if (filter2Value) {
        url += `&filter2=${encodeURIComponent(filter2Value)}`;
    }

    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            renderChartUI(container, data, templateSlug, district);
        })
        .catch(error => {
            console.error('Error fetching chart data:', error);
            container.innerHTML = `
                <div class="text-center text-red-500 py-10">
                    <i class="fas fa-exclamation-triangle fa-2x mb-2"></i>
                    <p>Failed to load chart data</p>
                    <p class="text-sm text-gray-500">${error.message}</p>
                </div>
            `;
        });
}

function renderChartUI(container, data, templateSlug, district) {
    // Build the outer HTML structure with filters if they don't exist yet
    let isInitialRender = !container.querySelector('.chart-header-controls');
    
    if (isInitialRender) {
        let filtersHtml = '';

        // Build filter1 dropdown
        if (data.filters && data.filters.filter1 && data.filters.filter1.options.length > 0) {
            const filter = data.filters.filter1;
            filtersHtml += `
                <div class="chart-filter-group flex items-center mb-2 justify-center md:justify-end">
                    <label class="mr-2 text-sm font-semibold text-gray-700">${filter.label}:</label>
                    <select class="dynamic-chart-filter p-1 border rounded min-w-[120px] text-sm focus:outline-none focus:ring-1 focus:ring-[#863F3F]" data-filter="1">
                        <option value="">All (Aggregated)</option>
                        ${filter.options.map(opt => `<option value="${opt}" ${opt === filter.selected ? 'selected' : ''}>${opt}</option>`).join('')}
                    </select>
                </div>
            `;
        }

        // Build filter2 dropdown
        if (data.filters && data.filters.filter2 && data.filters.filter2.options.length > 0) {
            const filter2 = data.filters.filter2;
            filtersHtml += `
                <div class="chart-filter-group flex items-center mb-2 justify-center md:justify-end">
                    <label class="mr-2 text-sm font-semibold text-gray-700">${filter2.label}:</label>
                    <select class="dynamic-chart-filter p-1 border rounded min-w-[120px] text-sm focus:outline-none focus:ring-1 focus:ring-[#863F3F]" data-filter="2">
                        <option value="">All (Aggregated)</option>
                        ${filter2.options.map(opt => `<option value="${opt}" ${opt === filter2.selected ? 'selected' : ''}>${opt}</option>`).join('')}
                    </select>
                </div>
            `;
        }

        const html = `
            <div class="chart-header-controls w-full flex flex-wrap gap-2 justify-end">
                ${filtersHtml}
            </div>
            <div class="chart-canvas-wrapper" style="position: relative; height: 100%; min-height: 350px;">
                <canvas></canvas>
            </div>
            ${data.description ? `<p class="mt-4 text-sm text-gray-600 text-left px-2">${data.description}</p>` : ''}
            ${data.additionalInfo ? `<p class="mt-1 text-xs text-gray-500 italic text-left px-2">${data.additionalInfo}</p>` : ''}
        `;
        
        container.innerHTML = html;
        
        // Add event listeners to filters — when any filter changes, re-fetch with both values
        const filterSelects = container.querySelectorAll('.dynamic-chart-filter');
        filterSelects.forEach(select => {
            select.addEventListener('change', () => {
                const f1Select = container.querySelector('.dynamic-chart-filter[data-filter="1"]');
                const f2Select = container.querySelector('.dynamic-chart-filter[data-filter="2"]');
                const f1Val = f1Select ? f1Select.value : null;
                const f2Val = f2Select ? f2Select.value : null;
                fetchAndRenderChart(container, templateSlug, district, f1Val, f2Val);
            });
        });
    } else {
        // Just hide the loader and restore opacity
        if (container.querySelector('.loading-indicator')) {
            container.querySelector('.loading-indicator').style.display = 'none';
        }
        container.querySelector('canvas').style.opacity = '1';
    }

    // Render the Chart.js canvas
    const canvas = container.querySelector('canvas');
    const ctx = canvas.getContext('2d');

    // Destroy existing chart if it exists
    if (container._chartInstance) {
        container._chartInstance.destroy();
    }

    // Prepare chart options based on data.chartOptions and defaults
    const isStacked = data.chartType === 'stackedBar' || data.chartType === 'percentStackedBar';
    const trueChartType = isStacked ? 'bar' : data.chartType;
    
    // Base configuration
    const config = {
        type: trueChartType,
        data: data.chartData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 15,
                        font: {
                            size: 11
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(255, 255, 255, 0.9)',
                    titleColor: '#000',
                    bodyColor: '#333',
                    borderColor: '#ddd',
                    borderWidth: 1,
                    padding: 10,
                    boxPadding: 4,
                    usePointStyle: true
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            },
            interaction: {
                mode: 'index',
                intersect: false,
            }
        }
    };

    // Apply stacking if needed
    if (isStacked) {
        config.options.scales.x.stacked = true;
        config.options.scales.y.stacked = true;
    }

    // Advanced features: if percent stacked bar
    if (data.chartType === 'percentStackedBar') {
        config.options.plugins.tooltip.callbacks = {
            label: function(context) {
                let label = context.dataset.label || '';
                if (label) {
                    label += ': ';
                }
                
                // Calculate percentage
                let total = 0;
                const dataArr = context.chart.data.datasets.map(d => d.data[context.dataIndex]);
                total = dataArr.reduce((a, b) => a + (b || 0), 0);
                
                const value = context.raw;
                const percentage = total > 0 ? Math.round((value / total) * 100) : 0;
                
                if (context.parsed.y !== null) {
                    label += value + ` (${percentage}%)`;
                }
                return label;
            }
        };
        // Ideally we would adjust Y-axis to 100%, but for a simple version we just stack normally
        // and adjust the tooltips to show percentages. A true 100% stacked bar is more complex in Chart.js.
    }

    // Merge in any custom options from the API
    if (data.chartOptions && typeof data.chartOptions === 'object') {
        mergeDeep(config.options, data.chartOptions);
    }

    // Create the chart
    container._chartInstance = new Chart(ctx, config);
}

// Simple object deep merge utility
function isObject(item) {
    return (item && typeof item === 'object' && !Array.isArray(item));
}

function mergeDeep(target, ...sources) {
    if (!sources.length) return target;
    const source = sources.shift();

    if (isObject(target) && isObject(source)) {
        for (const key in source) {
            if (isObject(source[key])) {
                if (!target[key]) Object.assign(target, { [key]: {} });
                mergeDeep(target[key], source[key]);
            } else {
                Object.assign(target, { [key]: source[key] });
            }
        }
    }
    return mergeDeep(target, ...sources);
}
