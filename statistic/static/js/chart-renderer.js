/**
 * Renders dynamic charts based on data fetched from the API.
 * Uses Chart.js for rendering.
 */

const LEGACY_DYNAMIC_CHART_STYLE_ID = 'legacy-dynamic-chart-style';
const PERCENT_LABEL_THRESHOLD = 5;

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

    ensureLegacyDynamicChartStyles();

    chartContainers.forEach(container => {
        initChart(container);
    });
});

function ensureLegacyDynamicChartStyles() {
    if (document.getElementById(LEGACY_DYNAMIC_CHART_STYLE_ID)) {
        return;
    }

    const style = document.createElement('style');
    style.id = LEGACY_DYNAMIC_CHART_STYLE_ID;
    style.textContent = `
        .dynamic-chart-container .chart-container {
            width: 100%;
            margin: 0 auto;
            background-color: #fff;
            position: relative;
            box-sizing: border-box;
            text-align: left;
        }

        .dynamic-chart-container .chart-filter-controls {
            display: flex;
            align-items: center;
            padding: 8px 8px 0 8px;
            border-radius: 1px;
        }

        .dynamic-chart-container .chart-filter-group {
            display: flex;
            align-items: center;
            margin-left: 45px;
            margin-right: 20px;
        }

        .dynamic-chart-container .chart-filter-group label {
            margin-right: 5px;
            font-size: 12px;
            color: #000;
        }

        .dynamic-chart-container .dynamic-chart-filter {
            color: #000;
            border: 0.4px solid #863F3F;
            border-radius: 4px;
            font-size: 12px;
            margin-left: 1px;
            width: 80px;
            min-width: 85px;
            background-color: #fff;
            padding: 1px 4px;
        }

        .dynamic-chart-container .dynamic-chart-filter:focus {
            outline: none;
            box-shadow: 0 0 0 1px rgba(134, 63, 63, 0.2);
        }

        .dynamic-chart-container .chart-canvas-container {
            width: 100%;
            height: auto;
            min-height: 400px;
            position: relative;
        }

        .dynamic-chart-container .chart-canvas-container canvas {
            width: 100% !important;
            height: 100% !important;
            display: block;
        }

        .dynamic-chart-container .chart-footer {
            display: flex;
            justify-content: space-between;
            margin-top: 10px;
            padding-top: 5px;
            border-top: 1px solid #e9ecef;
            text-align: left;
        }

        .dynamic-chart-container .chart-info {
            flex: 1;
            text-align: left;
        }

        .dynamic-chart-container .chart-description {
            margin-top: 0;
            padding: 2px;
            font-size: 10px;
            padding-left: 53px;
            color: #374151;
            text-align: left;
            display: block;
        }

        .dynamic-chart-container .chart-additional-info {
            margin-top: 2px;
            padding: 2px;
            font-size: 10px;
            padding-left: 53px;
            color: #4b5563;
            text-align: left;
            display: block;
        }

        @media (max-width: 767px) {
            .dynamic-chart-container .chart-filter-controls {
                justify-content: center;
                flex-direction: column;
                align-items: stretch;
            }

            .dynamic-chart-container .chart-filter-group {
                margin-left: 10px;
                margin-right: 0;
                justify-content: left;
                width: 100%;
            }

            .dynamic-chart-container .chart-filter-group label {
                font-size: 10px;
            }

            .dynamic-chart-container .dynamic-chart-filter {
                border: 0.1px solid #863F3F;
                font-size: 10px;
                width: 60px;
            }

            .dynamic-chart-container .chart-canvas-container {
                min-height: 300px;
            }

            .dynamic-chart-container .chart-description,
            .dynamic-chart-container .chart-additional-info {
                font-size: 9px;
                padding-left: 0;
            }
        }

        @media (min-width: 768px) and (max-width: 991px) {
            .dynamic-chart-container .chart-canvas-container {
                min-height: 400px;
            }

            .dynamic-chart-container .chart-filter-group {
                margin-left: 20px;
            }
        }
    `;

    document.head.appendChild(style);
}

function escapeHtml(value) {
    return String(value ?? '').replace(/[&<>'"]/g, (char) => {
        const entityMap = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#39;'
        };
        return entityMap[char] || char;
    });
}

function getSourceText(description) {
    const trimmed = String(description || '').trim();
    if (!trimmed) {
        return '';
    }
    return /^source\s*:/i.test(trimmed) ? trimmed : `Source: ${trimmed}`;
}

function formatIndianNumber(num) {
    if (num === null || num === undefined || isNaN(num)) return '';
    let isNegative = false;
    if (num < 0) {
        isNegative = true;
        num = Math.abs(num);
    }

    let formattedNumber;
    if (num >= 10000000) {
        const crValue = num / 10000000;
        formattedNumber = (crValue % 1 === 0 ? crValue.toString() : crValue.toFixed(2)) + 'Cr';
    } else if (num >= 100000) {
        const lValue = num / 100000;
        formattedNumber = (lValue % 1 === 0 ? lValue.toString() : lValue.toFixed(2)) + 'L';
    } else if (num >= 1000) {
        const kValue = num / 1000;
        formattedNumber = (kValue % 1 === 0 ? kValue.toString() : kValue.toFixed(2)) + 'K';
    } else {
        formattedNumber = num % 1 === 0 ? num.toString() : num.toFixed(2);
    }

    return isNegative ? '-' + formattedNumber : formattedNumber;
}

function formatAxisNumber(value, hideZero) {
    const numericValue = Number(value);
    if (!Number.isFinite(numericValue)) {
        return '';
    }
    if (hideZero && numericValue === 0) {
        return '';
    }

    if (Number.isInteger(numericValue)) {
        return String(numericValue);
    }

    return numericValue.toFixed(2).replace(/\.0+$/, '').replace(/(\.\d*[1-9])0+$/, '$1');
}

function formatPercentAxisTick(value) {
    const numericValue = Number(value);
    if (!Number.isFinite(numericValue)) {
        return '';
    }

    const rounded = Math.round(numericValue);
    if (rounded <= 0 || rounded > 100) {
        return '';
    }

    return rounded % 20 === 0 ? `${rounded}%`:'';
}

function registerChartDataLabelsIfAvailable() {
    if (typeof window === 'undefined' || !window.ChartDataLabels) {
        return false;
    }

    if (window.__dynamicChartDataLabelsRegistered) {
        return true;
    }

    try {
        Chart.register(window.ChartDataLabels);
        window.__dynamicChartDataLabelsRegistered = true;
        return true;
    } catch (error) {
        console.warn('Could not register ChartDataLabels plugin:', error);
        return false;
    }
}

function convertToPercentStackedData(chartData) {
    const percentData = {
        labels: Array.isArray(chartData.labels) ? [...chartData.labels] : [],
        datasets: Array.isArray(chartData.datasets)
            ? chartData.datasets.map((dataset) => ({
                ...dataset,
                data: Array.isArray(dataset.data) ? [...dataset.data] : [],
                _originalData: Array.isArray(dataset.data) ? [...dataset.data] : [],
            }))
            : [],
    };

    for (let labelIndex = 0; labelIndex < percentData.labels.length; labelIndex++) {
        let total = 0;

        for (let datasetIndex = 0; datasetIndex < percentData.datasets.length; datasetIndex++) {
            const rawValue = percentData.datasets[datasetIndex]._originalData[labelIndex];
            const numericValue = Number(rawValue);
            if (rawValue !== null && rawValue !== undefined && !Number.isNaN(numericValue)) {
                total += Math.abs(numericValue);
            }
        }

        for (let datasetIndex = 0; datasetIndex < percentData.datasets.length; datasetIndex++) {
            const rawValue = percentData.datasets[datasetIndex]._originalData[labelIndex];
            const numericValue = Number(rawValue);

            if (rawValue !== null && rawValue !== undefined && !Number.isNaN(numericValue) && total > 0) {
                percentData.datasets[datasetIndex].data[labelIndex] = (Math.abs(numericValue) / total) * 100;
            } else {
                percentData.datasets[datasetIndex].data[labelIndex] = 0;
            }
        }
    }

    return percentData;
}

function createLineHoverHighlightPlugin() {
    return {
        id: 'hoverHighlight',
        afterInit(chart) {
            chart.$origStyles = chart.data.datasets.map(ds => ({
                borderColor: ds.borderColor,
                backgroundColor: ds.backgroundColor,
                borderWidth: ds.borderWidth ?? 2,
                pointRadius: ds.pointRadius ?? 0,
                pointHoverRadius: ds.pointHoverRadius ?? 4,
            }));
            chart.$activeDataset = null;
            chart.$activeIndex = null;
            chart.$raf = null;
        },
        afterEvent(chart, args) {
            const e = args.event;
            if (!e || !chart.chartArea) {
                return;
            }

            const area = chart.chartArea;
            const inside = e.x >= area.left && e.x <= area.right && e.y >= area.top && e.y <= area.bottom;

            if (!inside || e.type === 'mouseout') {
                if (chart.$activeDataset != null) {
                    chart.data.datasets.forEach((ds, i) => {
                        const original = chart.$origStyles[i];
                        ds.borderColor = original.borderColor;
                        ds.backgroundColor = original.backgroundColor;
                        ds.borderWidth = original.borderWidth;
                        ds.pointRadius = original.pointRadius;
                        ds.pointHoverRadius = original.pointHoverRadius;
                    });
                    chart.$activeDataset = null;
                    chart.$activeIndex = null;
                    chart.update('none');
                }
                return;
            }

            if (chart.$raf) {
                return;
            }

            chart.$raf = requestAnimationFrame(() => {
                chart.$raf = null;

                const xScale = chart.scales.x;
                const yScale = chart.scales.y;
                if (!xScale || !yScale) {
                    return;
                }

                let xVal = xScale.getValueForPixel(e.x);
                let idx = 0;

                if (xScale.type === 'category') {
                    idx = Math.round(xVal);
                } else {
                    const labels = chart.data.labels.map(Number);
                    let best = Infinity;
                    for (let i = 0; i < labels.length; i++) {
                        const distance = Math.abs(xVal - labels[i]);
                        if (distance < best) {
                            best = distance;
                            idx = i;
                        }
                    }
                }

                idx = Math.max(0, Math.min(chart.data.labels.length - 1, idx));

                let winningDataset = -1;
                let bestDist = Infinity;

                chart.data.datasets.forEach((ds, di) => {
                    if (chart.getDatasetMeta(di).hidden) {
                        return;
                    }
                    const value = ds.data[idx];
                    if (value == null || isNaN(value)) {
                        return;
                    }
                    const yPixel = yScale.getPixelForValue(value);
                    const dist = Math.abs(e.y - yPixel);
                    if (dist < bestDist) {
                        bestDist = dist;
                        winningDataset = di;
                    }
                });

                if (winningDataset !== -1) {
                    let changed = false;

                    if (winningDataset !== chart.$activeDataset) {
                        chart.data.datasets.forEach((ds, di) => {
                            const original = chart.$origStyles[di];
                            if (di === winningDataset) {
                                ds.borderColor = original.borderColor;
                                ds.backgroundColor = original.backgroundColor;
                                ds.borderWidth = Math.max(2, original.borderWidth);
                            } else {
                                ds.borderColor = 'rgba(0,0,0,0.25)';
                                ds.backgroundColor = 'rgba(0,0,0,0.25)';
                                ds.borderWidth = original.borderWidth;
                            }
                        });
                        chart.$activeDataset = winningDataset;
                        changed = true;
                    }

                    if (idx !== chart.$activeIndex) {
                        chart.$activeIndex = idx;
                        changed = true;
                    }

                    if (changed) {
                        chart.update('none');
                    }
                }
            });
        },
        beforeTooltipDraw(chart) {
            const tooltip = chart.tooltip;
            if (!tooltip || !tooltip.dataPoints) {
                return;
            }
            const activeDataset = chart.$activeDataset;
            tooltip.labelTextColors = tooltip.dataPoints.map(point => (
                typeof activeDataset === 'number' && activeDataset !== point.datasetIndex
                    ? 'rgba(0,0,0,0.6)'
                    : '#000'
            ));
        },
    };
}

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
    if (container._chartInstance) {
        container._chartInstance.destroy();
        container._chartInstance = null;
    }

    // Show loading
    const loadingHtml = `
        <div class="loading-indicator text-center text-gray-500 py-10 flex flex-col items-center justify-center">
            <i class="fas fa-spinner fa-spin fa-2x mb-3 text-[#863F3F]"></i>
            <p class="text-sm">Loading chart data...</p>
        </div>
    `;

    container.innerHTML = loadingHtml;

    let url = `/api/chart-data/${templateSlug}/?district=${encodeURIComponent(district)}`;
    if (filter1Value !== null && filter1Value !== undefined && filter1Value !== '') {
        url += `&filter1=${encodeURIComponent(filter1Value)}`;
    }
    if (filter2Value !== null && filter2Value !== undefined && filter2Value !== '') {
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
    if (!data || !data.chartData || !Array.isArray(data.chartData.datasets)) {
        container.innerHTML = `
            <div class="text-center text-red-500 py-10">
                <i class="fas fa-exclamation-triangle fa-2x mb-2"></i>
                <p>Chart data is unavailable.</p>
            </div>
        `;
        return;
    }

    const showFilters = data.showFilters !== false;
    let filtersHtml = '';

    if (showFilters && data.filters && data.filters.filter1 && Array.isArray(data.filters.filter1.options) && data.filters.filter1.options.length > 0) {
        const filter = data.filters.filter1;
        filtersHtml += `
            <div class="chart-filter-group">
                <label>${escapeHtml(filter.label || filter.column || 'Filter')}:</label>
                <select class="dynamic-chart-filter" data-filter="1">
                    <option value="">All</option>
                    ${filter.options.map(opt => {
                        const selected = String(opt) === String(filter.selected || '') ? 'selected' : '';
                        return `<option value="${escapeHtml(opt)}" ${selected}>${escapeHtml(opt)}</option>`;
                    }).join('')}
                </select>
            </div>
        `;
    }

    if (showFilters && data.filters && data.filters.filter2 && Array.isArray(data.filters.filter2.options) && data.filters.filter2.options.length > 0) {
        const filter2 = data.filters.filter2;
        filtersHtml += `
            <div class="chart-filter-group">
                <label>${escapeHtml(filter2.label || filter2.column || 'Filter')}:</label>
                <select class="dynamic-chart-filter" data-filter="2">
                    <option value="">All</option>
                    ${filter2.options.map(opt => {
                        const selected = String(opt) === String(filter2.selected || '') ? 'selected' : '';
                        return `<option value="${escapeHtml(opt)}" ${selected}>${escapeHtml(opt)}</option>`;
                    }).join('')}
                </select>
            </div>
        `;
    }

    const sourceText = getSourceText(data.description);
    const hasFooter = Boolean(sourceText || data.additionalInfo);

    container.innerHTML = `
        <div class="chart-container">
            ${filtersHtml ? `<div class="chart-filter-controls">${filtersHtml}</div>` : ''}
            <div class="chart-canvas-container">
                <canvas></canvas>
            </div>
            ${hasFooter ? `
                <div class="chart-footer">
                    <div class="chart-info">
                        ${data.additionalInfo ? `<div class="chart-additional-info">${escapeHtml(data.additionalInfo)}</div>` : ''}
                        ${sourceText ? `<div class="chart-description">${escapeHtml(sourceText)}</div>` : ''}
                    </div>
                </div>
            ` : ''}
        </div>
    `;

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

    // Render the Chart.js canvas
    const canvas = container.querySelector('canvas');
    const ctx = canvas.getContext('2d');

    // Prepare chart options based on data.chartOptions and defaults
    const isPercentStacked = data.chartType === 'percentStackedBar';
    const isStacked = data.chartType === 'stackedBar' || data.chartType === 'percentStackedBar';
    const trueChartType = isStacked ? 'bar' : data.chartType;
    const isMobile = window.innerWidth < 768;
    const chartDataForRender = isPercentStacked ? convertToPercentStackedData(data.chartData) : data.chartData;

    // Process datasets for legacy line/bar chart styling
    if (chartDataForRender && chartDataForRender.datasets) {
        chartDataForRender.datasets.forEach(dataset => {
            if (trueChartType === 'line') {
                dataset.fill = false;
                dataset.tension = 0;
                dataset.borderWidth = 2;
                dataset.pointBackgroundColor = dataset.borderColor;
                dataset.spanGaps = false;

                const R_INACTIVE = 0;
                const R_LINE = 2;
                const R_POINT = 4;
                dataset.pointRadius = function(ctx) {
                    const activeDataset = ctx.chart.$activeDataset;
                    const activeIndex = ctx.chart.$activeIndex;
                    const datasetIndex = ctx.datasetIndex;
                    const dataIndex = ctx.dataIndex;

                    if (activeDataset === datasetIndex) {
                        return dataIndex === activeIndex ? R_POINT : R_LINE;
                    }
                    return R_INACTIVE;
                };
                dataset.pointHoverRadius = function(ctx) {
                    return dataset.pointRadius(ctx);
                };
                dataset.pointHoverBorderWidth = 0;
                dataset.pointHitRadius = 15; // invisible catch-area so hovering is easier
            } else if (trueChartType === 'bar' || trueChartType === 'stackedBar' || trueChartType === 'percentStackedBar') {
                dataset.borderWidth = 1;
                if (dataset.borderColor && !dataset.backgroundColor) {
                    dataset.backgroundColor = dataset.borderColor;
                }
            }
        });
    }

    // Base configuration matching ChartFlask exactly
    const config = {
        type: trueChartType,
        data: chartDataForRender,
        plugins: trueChartType === 'line' ? [createLineHoverHighlightPlugin()] : [],
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 40,
                easing: "easeInOutQuart",
            },
            interaction: {
                mode: 'index',
                intersect: false,
                axis: "x",
            },
            plugins: {
                legend: {
                    display: chartDataForRender.datasets.length > 1,
                    position: 'top',
                    align: 'center',
                    labels: {
                        boxWidth: 20,
                        boxHeight: 20,
                        padding: 15,
                        usePointStyle: true,
                        pointStyle: "rect",
                        font: { size: isMobile ? 10 : 12 },
                        color: '#333',
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(255, 255, 255, 0.4)',
                    titleColor: "black",
                    bodyColor: "black",
                    borderColor: 'rgba(0, 0, 0, 0.2)',
                    borderWidth: 1,
                    animation: { duration: 50, easing: "easeOutQuart" },
                    mode: "index",
                    intersect: false,
                    position: "nearest",
                    callbacks: {
                        label: function (context) {
                            let label = context.dataset.label || "";
                            if (label) {
                                label += ": ";
                            }
                            if (isPercentStacked) {
                                if (context.parsed.y !== null && context.parsed.y !== undefined) {
                                    label += context.parsed.y.toFixed(1)+'%';
                                }
                            } else {
                                if (context.parsed.y !== null) {
                                    const value = context.parsed.y;
                                    label += formatIndianNumber(value % 1 === 0 ? value : parseFloat(value.toFixed(2)));
                                }
                            }
                            return label;
                        }
                    }
                }
            },
            scales: {
                x: {
                    // offset: trueChartType === 'line',
                    offset: true,
                    grid: {
                        drawTicks: true,
                        drawOnChartArea: false,
                        color: 'rgba(0, 0, 0, 0.06)',
                        tickColor: 'rgba(0,0,0,0.5)',
                    },
                    ticks: {
                        color: '#333',
                        maxTicksLimit: isMobile ? 4 : 15,
                        font: { size: isMobile ? 10 : 12 },
                        callback: function(value) {
                            if (this.chart.scales.x.type === 'linear') {
                                const labels = (data.chartData.labels || []).map((label) => Number(label));
                                if (labels.includes(Number(value))) {
                                    return String(this.getLabelForValue(value)).replace(/,/g, '');
                                }
                                return null;
                            }
                            return String(this.getLabelForValue(value)).replace(/,/g, '');
                        }
                    }
                },
                y: {
                    beginAtZero: true,
                    grid: {
                        drawBorder: false,
                        tickColor: 'rgba(0,0,0,0.5)',
                        color: 'rgba(0, 0, 0, 0.06)'
                    },
                    ticks: {
                        callback: function (value) {
                            if (isPercentStacked) {
                                return formatPercentAxisTick(value);
                            }
                            return formatIndianNumber(value);
                        },
                        maxTicksLimit: 7,
                        color: '#333',
                        font: { size: isMobile ? 10 : 12 },
                    }
                }
            }
        }
    };

    if (isPercentStacked) {
        const hasDataLabels = registerChartDataLabelsIfAvailable();

        config.options.scales.y.min = 0;
        config.options.scales.y.max = 100;
        config.options.scales.y.ticks.stepSize = 20;

        if (hasDataLabels) {
            config.options.plugins.datalabels = {
                display: function(context) {
                    return Number(context.dataset.data[context.dataIndex]) > PERCENT_LABEL_THRESHOLD;
                },
                formatter: function(value) {
                    return Number(value).toFixed(1) + '%';
                },
                color: 'white',
                font: {
                    size: isMobile ? 6 : 12,
                },
                anchor: 'center',
                align: 'center',
            };
        }
    }

    // Apply stacking if needed
    if (isStacked) {
        config.options.scales.x.stacked = true;
        config.options.scales.y.stacked = true;
    }

    // Merge in any custom options from the API
    if (data.chartOptions && typeof data.chartOptions === 'object') {
        mergeDeep(config.options, data.chartOptions);
    }

    // Keep tick density and readability consistent across mobile and desktop.
    applyResponsiveTickSettings(config.options, chartDataForRender, isMobile, isPercentStacked);

    config.options.onHover = (event, activeElements, chart) => {
        if (!chart.canvas) {
            return;
        }

        const rect = chart.canvas.getBoundingClientRect();
        const x = event.native ? event.native.clientX - rect.left : event.x;
        const chartArea = chart.chartArea;

        if (x >= chartArea.left && x <= chartArea.right) {
            const canvasPosition = Chart.helpers.getRelativePosition(event, chart);
            const dataX = chart.scales.x.getValueForPixel(canvasPosition.x);
            const labels = chart.data.labels;

            let closestIndex = 0;
            let minDistance = Math.abs(dataX - 0);

            for (let i = 1; i < labels.length; i++) {
                const distance = Math.abs(dataX - i);
                if (distance < minDistance) {
                    minDistance = distance;
                    closestIndex = i;
                }
            }

            const tooltipElements = [];
            chart.data.datasets.forEach((dataset, datasetIndex) => {
                if (!chart.getDatasetMeta(datasetIndex).hidden && dataset.data[closestIndex] !== null && dataset.data[closestIndex] !== undefined) {
                    tooltipElements.push({
                        datasetIndex: datasetIndex,
                        index: closestIndex,
                    });
                }
            });

            if (tooltipElements.length > 0) {
                chart.tooltip.setActiveElements(tooltipElements, { x: canvasPosition.x, y: canvasPosition.y });
                chart.update('none');
            }
        } else {
            chart.tooltip.setActiveElements([], { x: 0, y: 0 });
            chart.update('none');
        }
    };

    // Create the chart
    container._chartInstance = new Chart(ctx, config);
}

function applyResponsiveTickSettings(options, chartData, isMobile, isPercentStacked) {
    const fontSize = isMobile ? 10 : 12;
    const maxXTickCount = isMobile ? 4 : 15;

    options.plugins = options.plugins || {};
    options.plugins.legend = options.plugins.legend || {};
    options.plugins.legend.labels = options.plugins.legend.labels || {};
    options.plugins.legend.labels.font = {
        ...(options.plugins.legend.labels.font || {}),
        size: fontSize,
    };

    options.scales = options.scales || {};
    options.scales.x = options.scales.x || {};
    options.scales.x.offset = true;
    options.scales.x.grid = {
        ...(options.scales.x.grid || {}),
        drawTicks: true,
        drawOnChartArea: false,
        color: 'rgba(0, 0, 0, 0.06)',
        tickColor: 'rgba(0,0,0,0.5)',
    };

    const xTickCallback = options.scales.x.ticks && typeof options.scales.x.ticks.callback === 'function'
        ? options.scales.x.ticks.callback
        : function(value) {
            if (this.chart.scales.x.type === 'linear') {
                const labels = (chartData.labels || []).map((label) => Number(label));
                if (labels.includes(Number(value))) {
                    return String(this.getLabelForValue(value)).replace(/,/g, '');
                }
                return null;
            }
            return String(this.getLabelForValue(value)).replace(/,/g, '');
        };

    options.scales.x.ticks = {
        ...(options.scales.x.ticks || {}),
        color: '#333',
        maxTicksLimit: maxXTickCount,
        font: {
            ...((options.scales.x.ticks && options.scales.x.ticks.font) || {}),
            size: fontSize,
        },
        callback: xTickCallback,
    };

    options.scales.y = options.scales.y || {};
    options.scales.y.grid = {
        ...(options.scales.y.grid || {}),
        color: 'rgba(0, 0, 0, 0.06)',
        drawBorder: false,
        tickColor: 'rgba(0,0,0,0.5)',
    };

    if (isPercentStacked) {
        options.scales.y.beginAtZero = true;
        options.scales.y.min = 0;
        options.scales.y.max = 100;
        options.scales.y.afterBuildTicks = function(axis) {
            axis.ticks = [0, 20, 40, 60, 80, 100].map((value) => ({ value }));
        };
    }

    options.scales.y.ticks = {
        ...(options.scales.y.ticks || {}),
        callback: function(value) {
            if (isPercentStacked) {
                return formatPercentAxisTick(value);
            }
            return formatIndianNumber(value);
        },
        maxTicksLimit: isPercentStacked ? 6 : 7,
        stepSize: isPercentStacked ? 20 : (options.scales.y.ticks && options.scales.y.ticks.stepSize),
        autoSkip: isPercentStacked ? false : (options.scales.y.ticks && options.scales.y.ticks.autoSkip),
        color: '#333',
        font: {
            ...((options.scales.y.ticks && options.scales.y.ticks.font) || {}),
            size: fontSize,
        },
    };
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
