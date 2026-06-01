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
    # Health
    'DSAPublicHospitals2': 'charthandler.DSAPublicHospitals2',
    'DSAPrivateHealth2': 'charthandler.DSAPrivateHealth2',
    'DSAAnganwadis': 'charthandler.DSAAnganwadis',
    'DSAPublicOutPatients': 'charthandler.DSAPublicOutPatients',
    'DSAReportedDeaths': 'charthandler.DSAReportedDeaths',
    'DSADeathCause': 'charthandler.DSADeathCause',
    'DSARegisteredBirths': 'charthandler.DSARegisteredBirths',
    'DSAFamilyWelfarePrograms': 'charthandler.DSAFamilyWelfarePrograms',
    'DSAVaccines': 'charthandler.DSAVaccines',
    'DSAMalnutrition2': 'charthandler.DSAMalnutrition2',
    'HMISPatients': 'charthandler.HMISPatients',
    'HMISDeliveries': 'charthandler.HMISDeliveries',
    'HMISMDeaths': 'charthandler.HMISMDeaths',
    'HMISCSection': 'charthandler.HMISCSection',
    'HMISSexRatio': 'charthandler.HMISSexRatio',
    'HMISAbortion': 'charthandler.HMISAbortion',
    'HMISAntenatalCare': 'charthandler.HMISAntenatalCare',
    'HMISFamilyPlanning': 'charthandler.HMISFamilyPlanning',
    'HMISContraceptives': 'charthandler.HMISContraceptives',
    'HMISInfantVaccinations': 'charthandler.HMISInfantVaccinations',
    'HMISIV2': 'charthandler.HMISIV2',
    'HMISInfantDeaths': 'charthandler.HMISInfantDeaths',
    'HMISInfantDeaths2': 'charthandler.HMISInfantDeaths2',
    'HMISChildDisease2': 'charthandler.HMISChildDisease2',
    'HMISAnaemia': 'charthandler.HMISAnaemia',
    'NFHSFacilities': 'charthandler.NFHSFacilities',
    'NFHSHighBloodSugar': 'charthandler.NFHSHighBloodSugar',
    'NFHSHypertension': 'charthandler.NFHSHypertension',
    'NFHSCancerScreening2': 'charthandler.NFHSCancerScreening2',
    'NFHSTobaccoAlcohol': 'charthandler.NFHSTobaccoAlcohol',
    'NFHSDeliveryExpenditure': 'charthandler.NFHSDeliveryExpenditure',
    'NFHSIFAConsumption': 'charthandler.NFHSIFAConsumption',
    'NFHSPostnatalCare': 'charthandler.NFHSPostnatalCare',
    'NFHSSexRatio': 'charthandler.NFHSSexRatio',
    'NFHSBirths': 'charthandler.NFHSBirths',
    'NFHSCSection': 'charthandler.NFHSCSection',
    'NFHSDiet': 'charthandler.NFHSDiet',
    'NFHSFamilyPlanning': 'charthandler.NFHSFamilyPlanning',
    'NFHSVaccinations': 'charthandler.NFHSVaccinations',
    'NFHSMalnutrition': 'charthandler.NFHSMalnutrition',
    'NFHSOverweight': 'charthandler.NFHSOverweight',
    'NFHSLowBMI': 'charthandler.NFHSLowBMI',
    'NFHSAnaemia': 'charthandler.NFHSAnaemia',
    # Industry
    'ECNumber': 'charthandler.ECNumber',
    'ECSocialGroup': 'charthandler.ECSocialGroup',
    'ECSourcesOfFinance': 'charthandler.ECSourcesOfFinance',
    'ECSourcesOfBorrowings': 'charthandler.ECSourcesOfBorrowings',
    'ECType': 'charthandler.ECType',
    'ECBroadActivity': 'charthandler.ECBroadActivity',
    'DSAMsme': 'charthandler.DSAMsme',
    'FactoryWorkers': 'charthandler.FactoryWorkers',
    'DSAElectricity': 'charthandler.DSAElectricity',
    'DSAPollutionCategory': 'charthandler.DSAPollutionCategory',
    # Labor
    'LaborWorkers': 'charthandler.LaborWorkers',
    'LaborAgeDistribution': 'charthandler.LaborAgeDistribution',
    'LaborECWorkers': 'charthandler.LaborECWorkers',
    'LaborECGender': 'charthandler.LaborECGender',
    'LaborECReligion': 'charthandler.LaborECReligion',
    'LaborMNREGAJobCards': 'charthandler.LaborMNREGAJobCards',
    'LaborMNREGAParticipation': 'charthandler.LaborMNREGAParticipation',
    'LaborMNREGAAccounts': 'charthandler.LaborMNREGAAccounts',
    'LaborMNREGAScope': 'charthandler.LaborMNREGAScope',
    'LaborGovtEmployees': 'charthandler.LaborGovtEmployees',
    'LaborDSAEstablishments': 'charthandler.LaborDSAEstablishments',
    'LaborDSAWorkers': 'charthandler.LaborDSAWorkers',
    'LaborIndustryType': 'charthandler.LaborIndustryType',
    
    # Demography — Population Profile
    'CensusPopulation': 'charthandler.CensusPopulation',
    'CensusAgeDistribution': 'charthandler.CensusAgeDistribution',
    'CensusSC': 'charthandler.CensusSC',
    'CensusST': 'charthandler.CensusST',
    'CensusLiterate': 'charthandler.CensusLiterate',
    'CensusWorking': 'charthandler.CensusWorking',
    'CensusMotherTongue': 'charthandler.CensusMotherTongue',
    'CensusReligion': 'charthandler.CensusReligion',
    'CensusSexRatio': 'charthandler.CensusSexRatio',
    # Demography — Household Characteristics
    'CensusToiletFacility': 'charthandler.CensusToiletFacility',
    'CensusCooking': 'charthandler.CensusCooking',
    'CensusWater': 'charthandler.CensusWater',
    'CensusElectricity': 'charthandler.CensusElectricity',
    'CensusTCAssets': 'charthandler.CensusTCAssets',
    'CensusOwnership': 'charthandler.CensusOwnership',
    # Demography — Migration
    'CensusInwardMigrationA': 'charthandler.CensusInwardMigrationA',
    'CensusInwardMigrationB': 'charthandler.CensusInwardMigrationB',
    'CensusInwardMigrationC': 'charthandler.CensusInwardMigrationC',
    'CensusInwardMigrationD': 'charthandler.CensusInwardMigrationD',
    'CensusInwardMigrationE': 'charthandler.CensusInwardMigrationE',
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

    has_filter1 = bool(template.filter1_column)
    has_filter2 = bool(template.filter2_column)
    disable_all_filter1 = template.chart_options.get('disable_all_filter1', template.chart_options.get('disable_aggregation', False))
    disable_all_filter2 = template.chart_options.get('disable_all_filter2', template.chart_options.get('disable_aggregation', False))
    
    # Build base queryset for filter options (district-scoped)
    base_district_qs = ModelClass.objects.filter(
        **{f'{template.main_filter_column}__iexact': district}
    ) if template.main_filter_column else ModelClass.objects.all()

    filter1_options = []
    filter2_options = []

    if has_filter1:
        filter1_options = list(
            base_district_qs.values_list(
                template.filter1_column, flat=True
            ).distinct().order_by(template.filter1_column)
        )
        # If aggregation is disabled and no filter1 is selected, default to the first option
        if disable_all_filter1 and not filter1_value and filter1_options:
            filter1_value = filter1_options[0]

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
        # If aggregation is disabled and no filter2 is selected, default to the first option
        if disable_all_filter2 and not filter2_value and filter2_options:
            filter2_value = filter2_options[0]

    # Build the data queryset with final filters
    queryset = base_district_qs

    # Apply secondary filter (taluka or select_facility etc)
    if filter1_value and template.filter1_column:
        queryset = queryset.filter(
            **{f'{template.filter1_column}__iexact': filter1_value}
        )

    # Apply tertiary filter
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

    # Determine if aggregation is needed (multi-row data without a filter selected)
    needs_aggregation = (
        (has_filter1 and not filter1_value) or
        (has_filter2 and not filter2_value)
    )

    if needs_aggregation:
        # Aggregate data by x-axis (year) — sum all sub-rows
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
    else:
        # Normal extraction without aggregation
        for record in queryset:
            x_value = getattr(record, x_column, None)
            if x_value is not None:
                if x_value not in labels:
                    labels.append(x_value)
                for col in y_columns:
                    value = getattr(record, col, None)
                    datasets_data[col].append(value)

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
        # Support both borderColor (line) and backgroundColor (bar) in dataset_config
        border_color = config.get('borderColor', default_colors[i % len(default_colors)])
        bg_color = config.get('backgroundColor', border_color)
        label = config.get('label', col.replace('_', ' ').title())

        is_bar = template.chart_type in ('bar', 'stackedBar', 'percentStackedBar')

        if is_bar:
            dataset = {
                'label': label,
                'data': datasets_data[col],
                'backgroundColor': bg_color,  # Original color
                'borderColor': bg_color,
                'borderWidth': 1,
            }
        else:
            dataset = {
                'label': label,
                'data': datasets_data[col],
                'borderColor': border_color,
                'backgroundColor': border_color + '33',  # 20% opacity fill
                'borderWidth': 2,
                'pointRadius': 4,
                'pointHoverRadius': 6,
                'fill': False,
            }

        datasets.append(dataset)

    # Build the response
    response_data = {
        'chartType': template.chart_type,
        'title': template.title,
        'showFilters': template.show_filters,
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
                'disableAllOption': disable_all_filter1,
            } if has_filter1 else None,
            'filter2': {
                'column': template.filter2_column,
                'label': template.filter2_column.replace('_', ' ').title() if template.filter2_column else '',
                'options': filter2_options,
                'selected': filter2_value,
                'disableAllOption': disable_all_filter2,
            } if has_filter2 else None,
        },
        'description': template.description,
        'additionalInfo': template.additional_info,
    }

    return JsonResponse(response_data)
