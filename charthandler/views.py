import json
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.apps import apps

from .models import ChartTemplate


# Data model registry — maps data_source_table values to actual model classes
DATA_MODEL_REGISTRY = {
    # Livestock & Fisheries
    'LivestockNumbers': 'charthandler.LivestockNumbers',
    'ArtificialInsemination': 'charthandler.ArtificialInsemination',
    'DairyCooperative': 'charthandler.DairyCooperative',
    'DairyByproduct': 'charthandler.DairyByproduct',
    'Fisheries': 'charthandler.Fisheries',
    'Veterinary': 'charthandler.Veterinary',
    # Agriculture
    'GrossCroppedArea': 'charthandler.GrossCroppedArea',
    'HoldingsArea': 'charthandler.HoldingsArea',
    'HoldingsNumber': 'charthandler.HoldingsNumber',
    'LandUse': 'charthandler.LandUse',
    'ChemicalFertilizer': 'charthandler.ChemicalFertilizer',
    'IrrigationBeneficiary': 'charthandler.IrrigationBeneficiary',
    'IrrigationFacilities': 'charthandler.IrrigationFacilities',
    'IrrigationProjects': 'charthandler.IrrigationProjects',
    'IrrigationWells': 'charthandler.IrrigationWells',
    'TubewellsHandpumps': 'charthandler.TubewellsHandpumps',
}


def _get_model_class(data_source_table):
    """Resolve a data source table name to a Django model class."""
    model_path = DATA_MODEL_REGISTRY.get(data_source_table)
    if not model_path:
        return None
    app_label, model_name = model_path.rsplit('.', 1)
    try:
        return apps.get_model(app_label, model_name)
    except LookupError:
        return None


def _format_indian_number(value):
    """Format a number in Indian style (Cr/L/K) for display."""
    if value is None:
        return None
    try:
        value = float(value)
    except (TypeError, ValueError):
        return value

    if abs(value) >= 10000000:  # 1 Cr
        return f"{value / 10000000:.2f} Cr"
    elif abs(value) >= 100000:  # 1 Lakh
        return f"{value / 100000:.2f} L"
    elif abs(value) >= 1000:  # 1 Thousand
        return f"{value / 1000:.2f} K"
    return str(round(value, 2))


@require_GET
def chart_data_api(request, template_slug):
    """
    API endpoint that returns chart data as JSON for a given ChartTemplate.

    Query parameters:
      - district: (required) District name to filter by
      - filter1: (optional) Secondary filter value (e.g. taluka)
      - filter2: (optional) Tertiary filter value (e.g. size_class)

    Returns Chart.js-compatible JSON response.
    """
    try:
        template = ChartTemplate.objects.get(slug=template_slug)
    except ChartTemplate.DoesNotExist:
        return JsonResponse({'error': 'Chart template not found'}, status=404)

    district = request.GET.get('district', '')
    filter1_value = request.GET.get('filter1', '')
    filter2_value = request.GET.get('filter2', '')

    if not district:
        return JsonResponse({'error': 'district parameter is required'}, status=400)

    # Resolve the data model
    ModelClass = _get_model_class(template.data_source_table)
    if not ModelClass:
        return JsonResponse({
            'error': f'Data source not found: {template.data_source_table}'
        }, status=500)

    # Build the queryset with filters
    queryset = ModelClass.objects.all()

    # Apply district filter (case-insensitive)
    if template.main_filter_column:
        queryset = queryset.filter(
            **{f'{template.main_filter_column}__iexact': district}
        )

    # Apply secondary filter (taluka)
    if filter1_value and template.filter1_column:
        queryset = queryset.filter(
            **{f'{template.filter1_column}__iexact': filter1_value}
        )

    # Apply tertiary filter (size_class, project_size, etc.)
    if filter2_value and template.filter2_column:
        queryset = queryset.filter(
            **{f'{template.filter2_column}__iexact': filter2_value}
        )

    # Get the x-axis values (typically years)
    x_column = template.x_column
    y_columns = template.y_columns or []

    # Order by x-axis column
    queryset = queryset.order_by(x_column)

    # Build the chart data
    labels = []
    datasets_data = {col: [] for col in y_columns}

    for record in queryset:
        x_value = getattr(record, x_column, None)
        if x_value is not None:
            # Avoid duplicate x-axis labels (for taluka-level data, aggregate)
            if x_value not in labels:
                labels.append(x_value)

            for col in y_columns:
                value = getattr(record, col, None)
                datasets_data[col].append(value)

    # If this has sub-filters, we need to aggregate when no filter is selected.
    has_filter1 = bool(template.filter1_column)
    has_filter2 = bool(template.filter2_column)
    filter1_options = []
    filter2_options = []

    # Build base queryset for filter options (district-scoped)
    base_district_qs = ModelClass.objects.filter(
        **{f'{template.main_filter_column}__iexact': district}
    ) if template.main_filter_column else ModelClass.objects.all()

    if has_filter1:
        filter1_options = list(
            base_district_qs.values_list(
                template.filter1_column, flat=True
            ).distinct().order_by(template.filter1_column)
        )

    if has_filter2:
        # Filter2 options are scoped by filter1 if filter1 is selected
        filter2_base_qs = base_district_qs
        if filter1_value and template.filter1_column:
            filter2_base_qs = filter2_base_qs.filter(
                **{f'{template.filter1_column}__iexact': filter1_value}
            )
        filter2_options = list(
            filter2_base_qs.values_list(
                template.filter2_column, flat=True
            ).distinct().order_by(template.filter2_column)
        )

    # Determine if aggregation is needed (multi-row data without a filter selected)
    needs_aggregation = (
        (has_filter1 and not filter1_value) or
        (has_filter2 and not filter2_value)
    )

    if needs_aggregation:
        # Aggregate data by x-axis (year) — sum all sub-rows
        labels = []
        datasets_data = {col: [] for col in y_columns}

        aggregated = {}
        for record in queryset:
            x_val = getattr(record, x_column, None)
            if x_val not in aggregated:
                aggregated[x_val] = {col: [] for col in y_columns}
            for col in y_columns:
                val = getattr(record, col, None)
                if val is not None:
                    aggregated[x_val][col].append(val)

        for x_val in sorted(aggregated.keys()):
            labels.append(x_val)
            for col in y_columns:
                values = aggregated[x_val][col]
                if values:
                    datasets_data[col].append(round(sum(values), 2))
                else:
                    datasets_data[col].append(None)

    # Convert integer labels for display
    labels = [int(l) if isinstance(l, float) and l == int(l) else l for l in labels]

    # Build datasets with colors from dataset_config
    dataset_configs = template.dataset_config or []
    default_colors = [
        '#1a4570', '#ee8939', '#2ca02c', '#d62728', '#9467bd',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
        '#ff6384', '#36a2eb', '#ffce56', '#4bc0c0', '#9966ff',
    ]

    datasets = []
    for i, col in enumerate(y_columns):
        config = dataset_configs[i] if i < len(dataset_configs) else {}
        color = config.get('borderColor', default_colors[i % len(default_colors)])
        label = config.get('label', col.replace('_', ' ').title())

        dataset = {
            'label': label,
            'data': datasets_data[col],
            'borderColor': color,
            'backgroundColor': color + '33',  # 20% opacity fill
            'borderWidth': 2,
            'pointRadius': 4,
            'pointHoverRadius': 6,
            'fill': False,
        }

        # Bar chart specific
        if template.chart_type in ('bar', 'stackedBar', 'percentStackedBar'):
            dataset['backgroundColor'] = color + 'CC'  # 80% opacity
            dataset['borderWidth'] = 1
            del dataset['pointRadius']
            del dataset['pointHoverRadius']
            del dataset['fill']

        datasets.append(dataset)

    # Build the response
    response_data = {
        'chartType': template.chart_type,
        'title': template.title,
        'chartOptions': template.chart_options,
        'chartData': {
            'labels': labels,
            'datasets': datasets,
        },
        'filters': {
            'filter1': {
                'column': template.filter1_column,
                'label': template.filter1_column.replace('_', ' ').title() if template.filter1_column else '',
                'options': filter1_options,
                'selected': filter1_value,
            } if has_filter1 else None,
            'filter2': {
                'column': template.filter2_column,
                'label': template.filter2_column.replace('_', ' ').title() if template.filter2_column else '',
                'options': filter2_options,
                'selected': filter2_value,
            } if has_filter2 else None,
        },
        'description': template.description,
        'additionalInfo': template.additional_info,
    }

    return JsonResponse(response_data)
