import pandas as pd
import re

df = pd.read_excel(r'c:\Users\vaibh\Desktop\CKA Projects\Chronical\Helth\Original_data\MH_health_website_graph_column_index.xlsx')
colors = ['#1a4570', '#e9ba5d', '#e46e53', '#00a3e0', '#8a2be2', '#228b22', '#ff8c00', '#dc143c', '#4682b4']

lines = []
lines.append('"""Management command to create the default Chart Templates for Health."""')
lines.append('from django.core.management.base import BaseCommand')
lines.append('from charthandler.models import ChartTemplate\n')
lines.append('def build_chart_options(y_axis_title, is_percent=False):')
lines.append('    options = {')
lines.append("        'scales': {")
lines.append("            'x': {'title': {'display': True, 'text': 'Year'}},")
lines.append("            'y': {'beginAtZero': True, 'title': {'display': True, 'text': y_axis_title}}")
lines.append('        }')
lines.append('    }')
lines.append('    if is_percent:')
lines.append("        options['scales']['y']['max'] = 100")
lines.append('    return options\n')

lines.append('class Command(BaseCommand):')
lines.append("    help = 'Creates/Updates Chart Templates for Health.'\n")
lines.append('    def handle(self, *args, **options):')
lines.append("        self.stdout.write('Creating Chart Templates for Health...')")
lines.append('        templates = [')

for idx, row in df.iterrows():
    title = str(row.get('Graph Title', ''))
    if title == 'nan' or not title.strip(): continue
    chart_type = row.get('Chart Type', 'line')
    source_sheet = str(row.get('Source Sheet', ''))
    model_name = source_sheet.replace(' ', '').replace('_', '').replace('(', '').replace(')', '') if source_sheet != 'nan' else ''
    y_axis_label = str(row.get('Website Dataset Labels', ''))
    dataset_cols_str = str(row.get('Dataset Columns Used in Excel', ''))
    
    x_col = 'year'
    main_filter = str(row.get('Main Filter Column', 'district')).strip().lower()
    if main_filter == 'nan': main_filter = 'district'
    
    dd1 = str(row.get('Dropdown 1 Column', ''))
    dd1_col = re.sub(r'[^a-z0-9]+', '_', dd1.strip().lower()).strip('_') if dd1 != 'nan' and dd1.strip() else ''
    dd2 = str(row.get('Dropdown 2 Column', ''))
    dd2_col = re.sub(r'[^a-z0-9]+', '_', dd2.strip().lower()).strip('_') if dd2 != 'nan' and dd2.strip() else ''
    
    labels = [l.strip() for l in y_axis_label.split(',') if l.strip() and l.strip() != 'nan'] if y_axis_label != 'nan' else []
    cols = [c.strip() for c in dataset_cols_str.split(';') if c.strip() and c.strip() != 'nan'] if dataset_cols_str != 'nan' else []
    
    y_columns = [re.sub(r'[^a-z0-9]+', '_', c.lower()).strip('_') for c in cols]
    show_filters = bool(dd1_col or dd2_col)
    
    is_percent = 'Percentage' in labels or chart_type == 'percentStackedBar'
    y_axis_title = 'Percentage' if is_percent else 'Number'
    
    prefix = source_sheet.split('_')[0] if '_' in source_sheet else ''
    source_text = 'Source: District Statistical Abstracts' if prefix == 'DSA' else ('Source: Health Management Information System' if prefix == 'HMIS' else ('Source: National Family Health Survey' if prefix == 'NFHS' else 'Source: Government Data'))
    
    lines.append('            {')
    lines.append(f"            'title': {repr(title)},")
    lines.append(f"            'chapter_type': 'health',")
    lines.append(f"            'chart_type': {repr(chart_type)},")
    lines.append(f"            'data_source_table': {repr(model_name)},")
    lines.append(f"            'x_column': {repr(x_col)},")
    lines.append(f"            'y_columns': {repr(y_columns)},")
    lines.append(f"            'dataset_config': [")
    for i, lbl in enumerate(labels):
        color = colors[i % len(colors)]
        lines.append(f"                {{'label': {repr(lbl)}, 'borderColor': '{color}', 'backgroundColor': '{color}'}},")
    lines.append(f"            ],")
    lines.append(f"            'main_filter_column': {repr(main_filter)},")
    lines.append(f"            'filter1_column': {repr(dd1_col)},")
    lines.append(f"            'filter2_column': {repr(dd2_col)},")
    lines.append(f"            'show_filters': {show_filters},")
    lines.append(f"            'chart_options': build_chart_options({repr(y_axis_title)}, {is_percent}),")
    lines.append(f"            'description': '',")
    lines.append(f"            'additional_info': {repr(source_text)},")
    lines.append(f"            'display_order': {idx + 1},")
    lines.append('            },')

lines.append('        ]')
lines.append('        count = 0')
lines.append('        updated = 0')
lines.append('        for config in templates:')
lines.append('            obj, created = ChartTemplate.objects.update_or_create(')
lines.append('                title=config["title"],')
lines.append('                chapter_type=config["chapter_type"],')
lines.append('                defaults=config')
lines.append('            )')
lines.append('            if created:')
lines.append('                count += 1')
lines.append('                self.stdout.write(f"  [NEW] {obj.title}")')
lines.append('            else:')
lines.append('                updated += 1')
lines.append('                self.stdout.write(f"  [UPD] {obj.title}")')
lines.append('')
lines.append('        expected_titles = {config["title"] for config in templates}')
lines.append('        stale_titles = list(')
lines.append('            ChartTemplate.objects')
lines.append('            .filter(chapter_type="health")')
lines.append('            .exclude(title__in=expected_titles)')
lines.append('            .values_list("title", flat=True)')
lines.append('        )')
lines.append('        if stale_titles:')
lines.append('            self.stdout.write(self.style.WARNING(')
lines.append('                "\\nStale health templates found (not touched by this command):\\n"')
lines.append('                + "\\n".join(f"  - {title}" for title in stale_titles)')
lines.append('            ))')
lines.append('')
lines.append('        self.stdout.write(self.style.SUCCESS(')
lines.append('            f"\\nDone! Processed {len(templates)} templates. ({count} new, {updated} updated)"')
lines.append('        ))')

with open(r'c:\Users\vaibh\Desktop\CKA Projects\Chronical\charthandler\management\commands\extract_health_templates.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print('Script finished.')
