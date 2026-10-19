"""
One-shot script to merge the DSA 2022-2024 staging rows into MH_health.xlsx.

Source: Original_data/2022-24 data/Maharashtra_Health_DSA_Staging_Batch{1-4}_2022-2024.xlsx
        (8 *_DSAH sheets in the raw DSA layout: old district names, raw counts,
        in/out-patients in hundreds)
Target: the 11 DSA_* sheets of Original_data/MH_health.xlsx (cleaned layout)

Each staging sheet is mapped/transformed into the master's layout and the new
rows are inserted right after each district's existing block; districts that
are new to the DSA sheets go after a fixed anchor district. All other sheets
are left untouched. The written file is then re-opened and verified against
the pre-merge master.

Usage:
    python Maharashtra/Health/merge_dsa_2022_24.py --out PATH [--report PATH]
    python Maharashtra/Health/merge_dsa_2022_24.py --verify-only --out PATH [--report PATH]

--master must point to the PRE-merge workbook (default: Original_data/MH_health.xlsx).
"""
import argparse
import glob
import os
import re
import sys
import zipfile
from collections import Counter, OrderedDict, defaultdict
from copy import copy

import openpyxl

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MASTER_PATH = os.path.join(BASE_DIR, 'Original_data', 'MH_health.xlsx')
STAGING_GLOB = os.path.join(BASE_DIR, 'Original_data', '2022-24 data',
                            'Maharashtra_Health_DSA_Staging_Batch*_2022-2024.xlsx')

NEW_YEARS = (2022, 2023, 2024)

# ── Name normalisation (staging → master) ──
DISTRICT_MAP = {
    'Ahmednagar': 'Ahilyanagar',
    'Buldana': 'Buldhana',
    'Osmanabad': 'Dharashiv',
    'Mumbai City': 'Mumbai',
    'Aurangabad': 'Chh. Sambhaji Nagar',
}
TALUKA_MAP = {
    'Buldana': 'Buldhana',
    'Osmanabad': 'Dharashiv',
    'Aurangabad': 'Chh. Sambhaji Nagar',
    'Andheri': 'Adheri',    # master's existing spelling, keeps the series continuous
    'Bokar': 'Bhokar',      # Nanded; spelled 'Bokar' in some staging sheets
}
NEW_DISTRICTS = ('Chh. Sambhaji Nagar', 'Jalgaon', 'Solapur')

# Most DSA sheets keep the raw workbook's district order (A-Z by the OLD names);
# ReportedDeaths, DeathCause and Anganwadis were re-sorted A-Z by current names.
AZ_SHEETS = {'DSA_ReportedDeaths', 'DSA_DeathCause', 'DSA_Anganwadis'}
ANCHORS_OLD_ORDER = {'Chh. Sambhaji Nagar': 'Amravati', 'Jalgaon': 'Hingoli', 'Solapur': 'Sindhudurg'}
ANCHORS_AZ = {'Chh. Sambhaji Nagar': 'Chandrapur', 'Jalgaon': 'Hingoli', 'Solapur': 'Sindhudurg'}
# Sheets whose talukas are sorted A-Z inside each year block
TALUKA_AZ_SHEETS = {'DSA_ReportedDeaths', 'DSA_Anganwadis'}

RU_ORDER = {
    'DSA_FamilyWelfarePrograms': ('Rural', 'Urban', 'Total'),
    'DSA_Vaccines': ('Rural', 'Urban', 'Total'),
    'DSA_Malnutrition': ('Rural', 'Urban', 'Total'),
    'DSA_RegisteredBirths': ('Rural', 'Urban', 'Total'),
    'DSA_ReportedDeaths': ('Total', 'Rural', 'Urban'),
    'DSA_Anganwadis': ('Total', 'Rural', 'Urban'),
}

# ── Master layout ──
MASTER_HEADERS = {
    'DSA_FamilyWelfarePrograms': ['District', 'Year', 'Taluka', 'Rural/Urban', 'Family Welfare Centers', 'Fertile Couples',
                                  'Male Sterilization Numbers', 'Female Sterilization Numbers', 'IUDs Inserted',
                                  'Other Family Planning Methods Used'],
    'DSA_Vaccines': ['District', 'Year', 'Taluka', 'Rural/Urban', 'DPT', 'Polio', 'BCG', 'Measles', 'D.T',
                     'Tetanus 10 years', 'Tetanus 16 years', 'Tetanus Pregnant Women', 'Pentavalent-3'],
    'DSA_Malnutrition (2)': ['District', 'Year', 'Taluka', 'Select Variable', 'Percentage'],
    'DSA_Malnutrition': ['District', 'Year', 'Taluka', 'Rural/Urban', 'Normal Weight', 'Moderate Acute Malnutrition',
                         'Severe Acute Malnutrition'],
    'DSA_RegisteredBirths': ['District', 'Year', 'Taluka', 'Rural/Urban', 'Boys', 'Girls', 'Total'],
    'DSA_ReportedDeaths': ['District', 'Year', 'Taluka', 'Rural/Urban', 'Number', 'Children', 'Infants'],
    'DSA_DeathCause': ['District', 'Year', 'Sex', 'Select Cause', 'Number'],
    'DSA_PublicHospitals (2)': ['District', 'Year', 'Taluka', 'Select Facility', 'Number'],
    'DSA_PrivateHealth (2)': ['District', 'Year', 'Taluka', 'Select Facility', 'Number'],
    'DSA_Anganwadis': ['District', 'Year', 'Taluka', 'Rural/Urban', 'Approved Anganwadis', 'Working Anganwadis',
                       'Anganwadi Workers', 'Self-Owned Buildings', 'Rental Buildings', 'Without Regular Building',
                       'Anganwadis with Toilets'],
    'DSA_PublicOutPatients': ['District', 'Year', 'Taluka', 'Type', 'Male', 'Female', 'Children'],
}
DSA_SHEETS = list(MASTER_HEADERS)

# ── Staging layout: {sheet: {column index: expected header (whitespace-collapsed)}} ──
STAGING_HEADERS = {
    'FamilyPlanning_DSAH': {
        3: 'Rural/ Urban/ Total', 4: 'Number of Family Welfare Centers', 5: 'Number of fertile couples',
        6: 'Vasectomy', 7: 'Tubectomy', 8: 'IUD', 9: 'Family Planning- other methods'},
    'Vaccines_DSAH': {
        3: 'Total/ Rural/ Urban', 4: 'Triple gluten', 5: 'Polio', 6: 'BCG', 7: 'Measles', 8: 'Vdiguni (D.T.)',
        9: 'Diptheria Vaccine- 10 years', 10: 'Diptheria Vaccine- 16 years',
        11: 'Diptheria Vaccine- Pregnant Women', 12: 'Pentavalate-3'},
    'NatalMortality_DSAH': {
        2: 'Taluka', 3: 'Total/ Rural/ Urban', 4: 'Number of live births - Boys', 5: 'Number of live births - Girl',
        6: 'Number of live births - Total', 7: 'Total number of deaths',
        8: 'Total number of child deaths (0 to 5 years age group)',
        9: 'Number of infant deaths (0 to 1 years age group)'},
    'Malnutrition_DSAH': {
        3: 'Rural/ Urban/ Total', 5: 'Number of Children weighed throughout the year',
        7: 'Babies at normal weight', 8: 'Moderate acute malnutrition (MAM) Infants',
        9: 'Severe acute malnutrition (MAM) Infants'},
    'Anganwadi_DSAH': {
        3: 'Rural/ Urban/ Total', 4: 'Number of approved Anganwadi', 5: 'Number of working Anganwadi',
        6: 'Number of Workers', 7: 'Self-owned buildings', 8: 'Rental buildings',
        9: 'Anganwadi without regular buildings', 10: 'Toilet having Anganwadis (No.)'},
    'PublicHealth_DSAH': {
        2: 'Taluka', 3: 'Number of Hospitals', 4: 'Number of Special Hospitals (Cancer, TB etc.)',
        5: 'Number of Clinics', 6: 'Number of Maternity Wards', 7: 'Number of Primary Health Centres',
        8: 'Number of sub-centres', 9: 'Number of doctors/Vaids', 10: 'Total number of Beds',
        11: 'Number of beds for women', 12: 'Number of beds for children',
        13: "Number of male inpatients treated ('00)", 14: "Number of female inpatients treated ('00)",
        15: "Number of children inpatients treated ('00)", 16: "Number of male outpatients treated ('00)",
        17: "Number of female outpatients treated ('00)", 18: "Number of children outpatients treated ('00)"},
    'PrivateHealth_DSAH': {
        2: 'Taluka', 3: 'Hospitals', 4: 'Special Hospitals(Cancer, T.B.E)', 5: 'Clinics', 6: 'Maternity Wards',
        7: 'Number of Beds'},
    'DeathCause_DSAH': {
        2: 'Sex', 3: 'Winter fever', 4: 'Typhoid fever', 5: 'Tuberculosis', 6: 'Pneumonia/respiratory disorders',
        7: 'Diarrhoea, diarrhoea, gastro', 8: 'Dengue', 9: 'Swine flu', 10: 'AIDS', 11: 'Heart disorder',
        12: 'Cancer', 13: 'Maternal death in childbirth', 14: 'Paralysis', 15: 'Kidney related', 16: 'Suicide',
        17: 'Traffic', 18: 'Electric shock', 19: 'Burns', 20: 'Other accidents', 21: 'Other reasons',
        23: 'Number of Males died', 24: 'Number of Females died', 25: 'Total death'},
}

# Wide (Rural/Urban/Total) sheets: master sheet -> (staging sheet, staging column per master value column)
WIDE_SPECS = {
    'DSA_FamilyWelfarePrograms': ('FamilyPlanning_DSAH', [4, 5, 6, 7, 8, 9]),
    'DSA_Vaccines': ('Vaccines_DSAH', [4, 5, 6, 7, 8, 9, 10, 11, 12]),
    'DSA_RegisteredBirths': ('NatalMortality_DSAH', [4, 5, 6]),
    'DSA_ReportedDeaths': ('NatalMortality_DSAH', [7, 8, 9]),
    'DSA_Anganwadis': ('Anganwadi_DSAH', [4, 5, 6, 7, 8, 9, 10]),
}
# Long sheets: master sheet -> (staging sheet, [(staging column, master label)])
LONG_SPECS = {
    'DSA_PublicHospitals (2)': ('PublicHealth_DSAH', [
        (3, 'Hospitals'), (4, 'Specialty Hospitals (Cancer, TB etc.)'), (5, 'Clinics'), (6, 'Maternity Wards'),
        (7, 'Primary Health Centres'), (8, 'Sub-Centres'), (9, 'Doctors/Vaids'), (10, 'Number of Beds'),
        (11, 'Beds for Women'), (12, 'Beds for Children')]),
    'DSA_PrivateHealth (2)': ('PrivateHealth_DSAH', [
        (3, 'Hospitals'), (4, 'Specialty Hospitals (Cancer, TB, etc)'), (5, 'Clinics'), (6, 'Maternity Wards'),
        (7, 'Number of Beds')]),
}
MALNUTRITION_LABELS = ['Infants at Normal Weight', 'Infants with Moderate Acute Malnutrition',
                       'Infants with Severe Acute Malnutrition']
DEATH_CAUSES = ['Winter Fever', 'Typhoid Fever', 'Tuberculosis', 'Pneumonia/ Respiratory disorders',
                'Diarrhoea or Gastro', 'Dengue', 'Swine Flu', 'AIDS', 'Heart Disorder', 'Cancer',
                'Maternal Death during Childbirth', 'Paralysis', 'Kidney Related', 'Suicide', 'Traffic',
                'Electric Shock', 'Burns', 'Other Accidents', 'Other Reasons']
SEX_ORDER = ('Total', 'Male', 'Female')
# Out-patients sheet: Type -> staging columns for Male, Female, Children (values in '00)
OUTPATIENT_COLS = {'Outpatient': (16, 17, 18), 'Inpatient': (13, 14, 15)}


class MergeError(Exception):
    pass


def norm_header(value):
    return ' '.join(str(value).split()) if value is not None else None


def clean_num(value, where):
    """Staging cell -> int/float/None; integral floats (2022.0) become int."""
    if value is None:
        return None
    if isinstance(value, bool):
        raise MergeError(f'Boolean value at {where}')
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value) if value.is_integer() else value
    if isinstance(value, str) and not value.strip():
        return None
    raise MergeError(f'Non-numeric value {value!r} at {where}')


def tidy(value):
    """Result of arithmetic -> drop float noise, int when whole."""
    value = round(value, 6)
    return int(value) if float(value).is_integer() else value


def group_of(sheet, row):
    """Block key of a master row: district, or (district, Type) for the two out-patient sections."""
    return (row[0], row[3]) if sheet == 'DSA_PublicOutPatients' else row[0]


def trim(row):
    row = list(row)
    while row and row[-1] is None:
        row.pop()
    return tuple(row)


# ─────────────────────────── staging ───────────────────────────

def load_staging():
    files = sorted(glob.glob(STAGING_GLOB))
    if len(files) != 4:
        raise MergeError(f'Expected 4 staging files, found {len(files)}: {files}')
    staging = defaultdict(list)     # staging sheet -> rows (lists, staging column positions kept)
    flags = []
    for path in files:
        wb = openpyxl.load_workbook(path, data_only=True)
        for sheet, expected in STAGING_HEADERS.items():
            ws = wb[sheet]
            header = [norm_header(c.value) for c in ws[1]]
            for idx, text in expected.items():
                if idx >= len(header) or header[idx] != text:
                    raise MergeError(f'{os.path.basename(path)} {sheet}: column {idx} header is '
                                     f'{header[idx] if idx < len(header) else None!r}, expected {text!r}')
            for r_idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
                if all(v is None or (isinstance(v, str) and not v.strip()) for v in row):
                    continue
                where = f'{os.path.basename(path)} {sheet} row {r_idx}'
                if not isinstance(row[0], str) or not isinstance(row[2], str):
                    raise MergeError(f'Missing district/taluka at {where}: {row[:4]}')
                row = list(row)
                district = row[0].strip()
                row[0] = DISTRICT_MAP.get(district, district)
                row[1] = clean_num(row[1], where)
                row[2] = row[2].strip()
                if sheet not in ('PublicHealth_DSAH', 'PrivateHealth_DSAH', 'DeathCause_DSAH'):
                    row[3] = row[3].strip()
                if row[1] not in NEW_YEARS:
                    raise MergeError(f'Unexpected year {row[1]!r} at {where}')
                row.append(where)   # kept last, for error messages
                staging[sheet].append(row)
        for row in wb['Review_Flags'].iter_rows(min_row=2, values_only=True):
            if any(v is not None for v in row):
                flags.append(row[:6])
    return staging, flags


# ─────────────────────────── master info ───────────────────────────

def read_master_info(wb):
    """Talukas per district, latest-year taluka order per (sheet, block) and current max rows."""
    info = {'talukas': defaultdict(dict), 'order': {}, 'districts': set(), 'labels': {}}
    spelling_year = {}
    for sheet in DSA_SHEETS:
        rows = list(wb[sheet].iter_rows(values_only=True))
        header = list(trim(rows[0]))
        if header != MASTER_HEADERS[sheet]:
            raise MergeError(f'{sheet}: master header {header} != expected {MASTER_HEADERS[sheet]}')
        data = [r for r in rows[1:] if r[0] is not None]
        latest = {}
        for r in data:
            info['districts'].add(r[0])
            if r[1] >= min(NEW_YEARS):
                raise MergeError(f'{sheet} already has {r[1]} rows - pass the pre-merge workbook as --master')
            g = group_of(sheet, r)
            latest[g] = max(latest.get(g, 0), r[1])
            if sheet != 'DSA_DeathCause':
                # if two spellings differ only by case, the latest year's spelling wins
                key = (r[0], r[2].lower())
                if r[1] >= spelling_year.get(key, 0):
                    spelling_year[key] = r[1]
                    info['talukas'][r[0]][r[2].lower()] = r[2]
        order = defaultdict(list)
        for r in data:
            g = group_of(sheet, r)
            if sheet != 'DSA_DeathCause' and r[1] == latest[g] and r[2] not in order[g]:
                order[g].append(r[2])
        info['order'][sheet] = order
        if sheet in ('DSA_Malnutrition (2)', 'DSA_PublicHospitals (2)', 'DSA_PrivateHealth (2)', 'DSA_DeathCause'):
            info['labels'][sheet] = {r[3] for r in data}
        if sheet in RU_ORDER:
            seqs = Counter()
            cur = []
            for r in data:
                key = (r[0], r[1], r[2])
                if cur and cur[0] != key:
                    seqs[tuple(cur[1:])] += 1
                    cur = []
                if not cur:
                    cur = [key]
                cur.append(r[3])
            seqs[tuple(cur[1:])] += 1
            if seqs.most_common(1)[0][0] != RU_ORDER[sheet]:
                raise MergeError(f'{sheet}: master Rural/Urban order is {seqs.most_common(2)}, expected {RU_ORDER[sheet]}')
    return info


# ─────────────────────────── build new rows ───────────────────────────

def normalise_talukas(staging, info):
    """Map staging taluka names onto the master's spelling (case-insensitive) in place."""
    unresolved = set()
    for sheet, rows in staging.items():
        if sheet == 'DeathCause_DSAH':
            continue
        for row in rows:
            district, taluka = row[0], TALUKA_MAP.get(row[2], row[2])
            if district in NEW_DISTRICTS:
                row[2] = taluka
                continue
            if district not in info['districts']:
                raise MergeError(f'Unknown district {district!r} at {row[-1]}')
            known = info['talukas'][district]
            if taluka.lower() not in known:
                unresolved.add((district, row[2]))
                continue
            row[2] = known[taluka.lower()]
    if unresolved:
        raise MergeError(f'Unresolved talukas (district, staging name): {sorted(unresolved)}')


def build_new_rows(staging, info):
    """Returns {master sheet: OrderedDict(block key -> [row tuples in final order])}."""
    records = defaultdict(list)   # master sheet -> [(block, year, taluka, sub_rank, staging_pos, values)]

    def check_unique(sheet, keys):
        dup = [k for k, c in Counter(keys).items() if c > 1]
        if dup:
            raise MergeError(f'{sheet}: duplicate staging keys {dup[:5]}')

    # Wide Rural/Urban/Total sheets
    for sheet, (src, cols) in WIDE_SPECS.items():
        check_unique(src, [(r[0], r[1], r[2], r[3]) for r in staging[src]])
        for pos, r in enumerate(staging[src]):
            if r[3] not in RU_ORDER[sheet]:
                raise MergeError(f'Unexpected Rural/Urban label {r[3]!r} at {r[-1]}')
            values = (r[0], r[1], r[2], r[3]) + tuple(clean_num(r[i], r[-1]) for i in cols)
            records[sheet].append((r[0], r[1], r[2], RU_ORDER[sheet].index(r[3]), pos, values))

    # Malnutrition: % of children weighed, rounded to 2 decimals; (2) = Total rows melted
    src = 'Malnutrition_DSAH'
    check_unique(src, [(r[0], r[1], r[2], r[3]) for r in staging[src]])
    for pos, r in enumerate(staging[src]):
        weighed = clean_num(r[5], r[-1])
        pcts = []
        for i in (7, 8, 9):
            count = clean_num(r[i], r[-1])
            pcts.append(None if not weighed or count is None else tidy(round(count / weighed * 100, 2)))
        values = (r[0], r[1], r[2], r[3]) + tuple(pcts)
        records['DSA_Malnutrition'].append((r[0], r[1], r[2], RU_ORDER['DSA_Malnutrition'].index(r[3]), pos, values))
        if r[3] == 'Total':
            for k, (label, pct) in enumerate(zip(MALNUTRITION_LABELS, pcts)):
                if pct is not None:
                    records['DSA_Malnutrition (2)'].append((r[0], r[1], r[2], k, pos, (r[0], r[1], r[2], label, pct)))

    # Long facility sheets: blanks dropped, zeros kept
    for sheet, (src, cols) in LONG_SPECS.items():
        check_unique(src, [(r[0], r[1], r[2]) for r in staging[src]])
        for pos, r in enumerate(staging[src]):
            for k, (i, label) in enumerate(cols):
                v = clean_num(r[i], r[-1])
                if v is not None:
                    records[sheet].append((r[0], r[1], r[2], k, pos, (r[0], r[1], r[2], label, v)))

    # Out-patients / in-patients ('00 -> persons); rows kept even when blank
    for pos, r in enumerate(staging['PublicHealth_DSAH']):
        for typ, cols in OUTPATIENT_COLS.items():
            vals = []
            for i in cols:
                v = clean_num(r[i], r[-1])
                vals.append(None if v is None else tidy(v * 100))
            records['DSA_PublicOutPatients'].append(((r[0], typ), r[1], r[2], 0, pos, (r[0], r[1], r[2], typ) + tuple(vals)))

    # Death causes: district level, Total / Male / Female, blanks dropped
    src = 'DeathCause_DSAH'
    check_unique(src, [(r[0], r[1], r[2]) for r in staging[src]])
    for pos, r in enumerate(staging[src]):
        if r[2] not in SEX_ORDER:
            raise MergeError(f'Unexpected Sex {r[2]!r} at {r[-1]}')
        for k, cause in enumerate(DEATH_CAUSES):
            v = clean_num(r[3 + k], r[-1])
            if v is not None:
                records['DSA_DeathCause'].append((r[0], r[1], None, (SEX_ORDER.index(r[2]), k), pos,
                                                  (r[0], r[1], r[2], cause, v)))

    # Every label must already exist in the master sheet
    for sheet, labels in info['labels'].items():
        bad = {rec[5][3] for rec in records[sheet]} - labels
        if bad:
            raise MergeError(f'{sheet}: labels not in master: {bad}')

    # Order: block -> year -> taluka (master's latest-year order / A-Z) -> sub order
    new_rows = {}
    for sheet in DSA_SHEETS:
        first_seen = {}
        for block, year, taluka, sub, pos, values in records[sheet]:
            first_seen.setdefault((block, taluka), pos)

        def key(rec, sheet=sheet, first_seen=first_seen):
            block, year, taluka, sub, pos, values = rec
            if taluka is None:
                t_rank = (0,)
            elif sheet in TALUKA_AZ_SHEETS:
                t_rank = (0, taluka)
            else:
                order = info['order'][sheet].get(block, [])
                t_rank = (0, order.index(taluka)) if taluka in order else (1, first_seen[(block, taluka)])
            return (year, t_rank, sub)

        blocks = OrderedDict()
        for rec in records[sheet]:
            blocks.setdefault(rec[0], []).append(rec)
        new_rows[sheet] = OrderedDict(
            (block, [rec[5] for rec in sorted(recs, key=key)]) for block, recs in blocks.items())
    return new_rows


# ─────────────────────────── write ───────────────────────────

def anchor_of(sheet, block):
    district = block[0] if isinstance(block, tuple) else block
    anchors = ANCHORS_AZ if sheet in AZ_SHEETS else ANCHORS_OLD_ORDER
    anchor = anchors[district]
    return (anchor, block[1]) if isinstance(block, tuple) else anchor


def filter_hidden_rule(ws):
    """Returns f(values) -> True if the sheet's active autofilter would hide that row."""
    criteria = []
    for fc in ws.auto_filter.filterColumn:
        if fc.customFilters or fc.top10 or fc.dynamicFilter or fc.colorFilter or fc.iconFilter:
            raise MergeError(f'{ws.title}: unsupported autofilter type on column {fc.colId}')
        if fc.filters is not None:
            criteria.append((fc.colId, {str(f) for f in fc.filters.filter}))
    if not criteria:
        return lambda values: False
    return lambda values: not all(str(values[col]) in allowed for col, allowed in criteria)


def insert_rows(ws, sheet, new_blocks):
    """Rewrite rows 2.. with each block's new rows placed right after the block. Returns new last row."""
    n_cols = len(MASTER_HEADERS[sheet])
    old_max = ws.max_row
    cells = defaultdict(dict)
    for (r, c), cell in ws._cells.items():
        if r >= 2:
            if cell.hyperlink is not None or cell.comment is not None:
                raise MergeError(f'{sheet}!{cell.coordinate} has a hyperlink/comment; not handled')
            cells[r][c] = (cell._value, cell.data_type, copy(cell._style))
    dims = {r: d for r, d in ws.row_dimensions.items() if r >= 2}
    if ws.merged_cells.ranges or ws.conditional_formatting or ws.data_validations.dataValidation:
        raise MergeError(f'{sheet}: merged cells / conditional formats / validations are not handled')

    # Block runs of the existing rows
    last_row_of = OrderedDict()
    prev = None
    for r in range(2, old_max + 1):
        vals = {c: v[0] for c, v in cells[r].items()}
        if vals.get(1) is None:
            raise MergeError(f'{sheet}: empty row {r} inside the data')
        block = group_of(sheet, [vals.get(c) for c in range(1, n_cols + 1)])
        if block != prev and block in last_row_of:
            raise MergeError(f'{sheet}: block {block} is not contiguous (row {r})')
        last_row_of[block] = r
        prev = block

    pending = OrderedDict(new_blocks)
    anchored = defaultdict(list)
    for block in list(pending):
        if block not in last_row_of:
            district = block[0] if isinstance(block, tuple) else block
            if district not in NEW_DISTRICTS:
                raise MergeError(f'{sheet}: district block {block} missing from master')
            anchor = anchor_of(sheet, block)
            if anchor not in last_row_of:
                raise MergeError(f'{sheet}: anchor {anchor} missing')
            anchored[anchor].append(block)

    plan = []   # ('old', r) | ('new', values, template row)
    end_of_block = {r: b for b, r in last_row_of.items()}
    for r in range(2, old_max + 1):
        plan.append(('old', r))
        if r in end_of_block:
            block = end_of_block[r]
            for values in pending.pop(block, []):
                plan.append(('new', values, r))
            for new_block in anchored.get(block, []):
                for values in pending.pop(new_block):
                    plan.append(('new', values, r))
    if pending:
        raise MergeError(f'{sheet}: blocks not placed: {list(pending)}')

    hidden_by_filter = filter_hidden_rule(ws)

    for key in [k for k in ws._cells if k[0] >= 2]:
        del ws._cells[key]
    for key in [k for k in ws.row_dimensions if k >= 2]:
        del ws.row_dimensions[key]

    for i, item in enumerate(plan, start=2):
        if item[0] == 'old':
            r = item[1]
            for c, (value, data_type, style) in cells[r].items():
                cell = ws.cell(row=i, column=c)
                cell._value = value
                cell.data_type = data_type
                cell._style = copy(style)
            if r in dims:
                d = copy(dims[r])
                d.index = i
                ws.row_dimensions[i] = d
        else:
            _, values, template = item
            for c, (_, _, style) in cells[template].items():
                ws.cell(row=i, column=c)._style = copy(style)
            for c in range(1, n_cols + 1):
                ws.cell(row=i, column=c).value = values[c - 1]
            d = copy(dims[template]) if template in dims else ws.row_dimensions[i]
            d.index = i
            d.hidden = hidden_by_filter(values)
            ws.row_dimensions[i] = d

    new_max = len(plan) + 1
    if ws.max_row != new_max:
        raise MergeError(f'{sheet}: max_row {ws.max_row} != expected {new_max}')

    def extend(ref, what):
        m = re.fullmatch(r'(\$?A\$?1:\$?[A-Z]+\$?)(\d+)', ref)
        if not m or int(m.group(2)) != old_max:
            raise MergeError(f'{sheet}: {what} range {ref!r} does not end at the old last row {old_max}')
        return f'{m.group(1)}{new_max}'

    if ws.auto_filter.ref:
        ws.auto_filter.ref = extend(ws.auto_filter.ref, 'autofilter')
    for table in ws.tables.values():
        table.ref = extend(table.ref, f'table {table.name}')
        if table.autoFilter is not None:
            table.autoFilter.ref = extend(table.autoFilter.ref, f'table {table.name} autofilter')
    for name, dn in ws.defined_names.items():
        sheet_part, _, rng = dn.attr_text.rpartition('!')
        dn.attr_text = f'{sheet_part}!{extend(rng, f"defined name {name}")}'
    return new_max


def write_merged(master_path, out_path):
    wb = openpyxl.load_workbook(master_path)     # data_only=False: keeps the HMIS formulas
    info = read_master_info(wb)
    staging, flags = load_staging()
    normalise_talukas(staging, info)
    new_rows = build_new_rows(staging, info)
    for sheet in DSA_SHEETS:
        last = insert_rows(wb[sheet], sheet, new_rows[sheet])
        print(f'  [OK] {sheet}: +{sum(len(v) for v in new_rows[sheet].values())} rows, last row {last}')
    wb.save(out_path)
    print(f'Saved {out_path}')


# ─────────────────────────── verify ───────────────────────────

def sheet_rows(ws):
    rows = [trim(r) for r in ws.iter_rows(values_only=True)]
    while rows and not rows[-1]:
        rows.pop()
    return rows


def verify(master_path, out_path):
    errors, report = [], []

    def check(ok, msg):
        if not ok:
            errors.append(msg)

    orig = openpyxl.load_workbook(master_path, read_only=True)
    info = read_master_info(orig)
    staging, flags = load_staging()
    normalise_talukas(staging, info)
    expected = build_new_rows(staging, info)
    new = openpyxl.load_workbook(out_path, read_only=True)

    # 1. Untouched sheets identical
    check(orig.sheetnames == new.sheetnames, 'Sheet list changed')
    for sheet in orig.sheetnames:
        if sheet in MASTER_HEADERS:
            continue
        check(sheet_rows(orig[sheet]) == sheet_rows(new[sheet]), f'{sheet}: contents changed')
    report.append(f'Untouched sheets compared cell by cell: {len(orig.sheetnames) - len(DSA_SHEETS)}')

    report.append('')
    report.append(f'{"Sheet":28s} {"before":>8s} {"added":>7s} {"after":>8s}   ' + '  '.join(str(y) for y in NEW_YEARS))
    new_sheet_rows = {}
    for sheet in DSA_SHEETS:
        o_rows, n_rows = sheet_rows(orig[sheet]), sheet_rows(new[sheet])
        n_cols = len(MASTER_HEADERS[sheet])
        new_sheet_rows[sheet] = n_rows
        exp_new = [trim(v) for block in expected[sheet].values() for v in block]

        # 2. Old rows unchanged and in the same order; 3. new rows as expected
        old_part = [r for r in n_rows[1:] if r[1] not in NEW_YEARS]
        new_part = [r for r in n_rows[1:] if r[1] in NEW_YEARS]
        check(n_rows[0] == o_rows[0], f'{sheet}: header row changed')
        check(old_part == o_rows[1:], f'{sheet}: existing rows changed or reordered')
        check(sorted(map(repr, new_part)) == sorted(map(repr, exp_new)), f'{sheet}: new rows differ from staging')
        check(len(n_rows) == len(o_rows) + len(exp_new), f'{sheet}: row count {len(n_rows)} != {len(o_rows)} + {len(exp_new)}')
        check(all(len(r) <= n_cols for r in new_part), f'{sheet}: new rows have values beyond the header')

        # 4. Layout: contiguous blocks, years ascending, new rows directly after their block / anchor
        runs, seen = [], set()
        for r in n_rows[1:]:
            b = group_of(sheet, r)
            if not runs or runs[-1][0] != b:
                check(b not in seen, f'{sheet}: block {b} not contiguous')
                seen.add(b)
                runs.append([b, []])
            runs[-1][1].append(r)
        for b, rows in runs:
            years = [r[1] for r in rows]
            check(years == sorted(years), f'{sheet}: years not ascending in block {b}')
            if b in expected[sheet]:
                exp_block = [trim(v) for v in expected[sheet][b]]
                check(rows[len(rows) - len(exp_block):] == exp_block, f'{sheet}: new rows of {b} not at the end of its block')
        order = [b for b, _ in runs]
        for b in expected[sheet]:
            district = b[0] if isinstance(b, tuple) else b
            if district in NEW_DISTRICTS:
                anchor = anchor_of(sheet, b)
                check(order.index(b) == order.index(anchor) + 1, f'{sheet}: {b} is not right after {anchor}')

        # 5. Names
        for r in new_part:
            for v in r[:4]:
                check(not isinstance(v, str) or v == v.strip(), f'{sheet}: stray whitespace in {r[:4]}')
            if sheet != 'DSA_DeathCause' and r[0] not in NEW_DISTRICTS:
                check(r[2].lower() in info['talukas'][r[0]] and info['talukas'][r[0]][r[2].lower()] == r[2],
                      f'{sheet}: taluka {r[:3]} not in master')
        districts = {r[0] for r in n_rows[1:]}
        check(districts == info['districts'] | set(NEW_DISTRICTS), f'{sheet}: district set {sorted(districts)}')

        # 6. Numbers: int years, no float noise
        for r in new_part:
            check(type(r[1]) is int, f'{sheet}: non-int year in {r[:4]}')
            for v in r[4:]:
                check(v is None or (isinstance(v, (int, float)) and abs(v * 100 - round(v * 100)) < 1e-6),
                      f'{sheet}: odd value {v!r} in {r[:4]}')

        by_year = Counter(r[1] for r in new_part)
        report.append(f'{sheet:28s} {len(o_rows) - 1:8d} {len(new_part):7d} {len(n_rows) - 1:8d}   '
                      + '  '.join(f'{by_year[y]:4d}' for y in NEW_YEARS))

    # 6b. Independent totals: staging column sums == merged new-row sums
    def new_sum(sheet, col, where=lambda r: True):
        rows = [r for r in new_sheet_rows[sheet][1:] if r[1] in NEW_YEARS and where(r)]
        vals = [r[col] for r in rows if col < len(r) and r[col] is not None]
        return len(vals), sum(vals)

    def stg_sum(src, idx, where=lambda r: True, factor=1):
        vals = [clean_num(r[idx], r[-1]) for r in staging[src] if where(r)]
        vals = [v * factor for v in vals if v is not None]
        return len(vals), sum(vals)

    def same(a, b):
        return a[0] == b[0] and abs(a[1] - b[1]) < 1e-6 * max(1, abs(b[1]))

    for sheet, (src, cols) in WIDE_SPECS.items():
        for j, idx in enumerate(cols):
            a, b = new_sum(sheet, 4 + j), stg_sum(src, idx)
            check(same(a, b), f'{sheet}.{MASTER_HEADERS[sheet][4 + j]}: merged {a} vs staging {b}')
    for sheet, (src, cols) in LONG_SPECS.items():
        for idx, label in cols:
            a, b = new_sum(sheet, 4, lambda r, l=label: r[3] == l), stg_sum(src, idx)
            check(same(a, b), f'{sheet}.{label}: merged {a} vs staging {b}')
    for typ, cols in OUTPATIENT_COLS.items():
        for j, idx in enumerate(cols):
            a = new_sum('DSA_PublicOutPatients', 4 + j, lambda r, t=typ: r[3] == t)
            b = stg_sum('PublicHealth_DSAH', idx, factor=100)
            check(same(a, b), f'DSA_PublicOutPatients.{typ}.{j}: merged {a} vs staging x100 {b}')
    for k, cause in enumerate(DEATH_CAUSES):
        for sex in SEX_ORDER:
            a = new_sum('DSA_DeathCause', 4, lambda r, c=cause, s=sex: r[3] == c and r[2] == s)
            b = stg_sum('DeathCause_DSAH', 3 + k, lambda r, s=sex: r[2] == s)
            check(same(a, b), f'DSA_DeathCause.{sex}.{cause}: merged {a} vs staging {b}')
    # Malnutrition recomputed straight from the counts
    mal = {(r[0], r[1], r[2], r[3]): r for r in new_sheet_rows['DSA_Malnutrition'][1:] if r[1] in NEW_YEARS}
    for r in staging['Malnutrition_DSAH']:
        got = mal[(r[0], r[1], r[2], r[3])]
        w = clean_num(r[5], r[-1])
        for j, i in enumerate((7, 8, 9)):
            c = clean_num(r[i], r[-1])
            exp = None if not w or c is None else round(c / w * 100, 2)
            g = got[4 + j] if 4 + j < len(got) else None
            check((exp is None and g is None) or (exp is not None and g is not None and abs(g - exp) < 1e-9),
                  f'DSA_Malnutrition {got[:4]}: {g} vs recomputed {exp}')

    # 7. Package structure: tables, autofilters, defined names end at the new last row
    with zipfile.ZipFile(out_path) as z:
        wb_xml = z.read('xl/workbook.xml').decode('utf8')
        tables = {re.search(r' name="([^"]+)"', z.read(n).decode('utf8')).group(1):
                  re.search(r' ref="([^"]+)"', z.read(n).decode('utf8')).group(1)
                  for n in z.namelist() if n.startswith('xl/tables/')}
    for sheet in DSA_SHEETS:
        last = len(new_sheet_rows[sheet])
        for m in re.finditer(r"<definedName [^>]*>'?" + re.escape(sheet) + r"'?!([^<]+)</definedName>", wb_xml):
            check(re.search(r'(\d+)$', m.group(1)).group(1) == str(last),
                  f'{sheet}: defined name range {m.group(1)} not ending at row {last}')
    for name, ref in tables.items():
        sheet = {'DSA_Malnutrition': 'DSA_Malnutrition (2)', 'DSA_PublicHospitals': 'DSA_PublicHospitals (2)',
                 'DSA_PrivateHealth': 'DSA_PrivateHealth (2)'}.get(name)
        if sheet:
            check(ref.endswith(str(len(new_sheet_rows[sheet]))), f'table {name} ref {ref}')
    report.append('')
    report.append('Table ranges: ' + ', '.join(f'{k}={v}' for k, v in sorted(tables.items())))

    # 8. Report details
    report.append('')
    report.append('New districts (2022-2024 only): ' + ', '.join(NEW_DISTRICTS))
    report.append('')
    report.append('New rows per district and year (DSA_Vaccines / DSA_DeathCause / DSA_PublicOutPatients):')
    counts = defaultdict(Counter)
    for sheet in ('DSA_Vaccines', 'DSA_DeathCause', 'DSA_PublicOutPatients'):
        for r in new_sheet_rows[sheet][1:]:
            if r[1] in NEW_YEARS:
                counts[(r[0], sheet)][r[1]] += 1
    for district in sorted({d for d, _ in counts}):
        cells = []
        for sheet in ('DSA_Vaccines', 'DSA_DeathCause', 'DSA_PublicOutPatients'):
            c = counts[(district, sheet)]
            cells.append('/'.join(str(c[y]) for y in NEW_YEARS))
        report.append(f'  {district:22s} ' + '   '.join(f'{x:>12s}' for x in cells))

    blank_op = Counter((r[0], r[1], r[3]) for r in new_sheet_rows['DSA_PublicOutPatients'][1:]
                       if r[1] in NEW_YEARS and all(v is None for v in (list(r) + [None] * 3)[4:7]))
    report.append('')
    report.append('DSA_PublicOutPatients rows left blank (PDF printed only a merged figure / no data):')
    for (d, y, t), c in sorted(blank_op.items()):
        report.append(f'  {d} {y} {t}: {c} talukas')

    # DeathCause: causes vs printed totals (source arithmetic, informational)
    mism = []
    for r in staging['DeathCause_DSAH']:
        causes = [clean_num(r[3 + k], r[-1]) for k in range(len(DEATH_CAUSES))]
        printed = clean_num(r[25] if r[2] == 'Total' else (r[23] if r[2] == 'Male' else r[24]), r[-1])
        s = sum(v for v in causes if v is not None)
        if printed is not None and s != printed:
            mism.append(f'{r[0]} {r[1]} {r[2]}: causes sum {s} vs printed {printed}')
    report.append('')
    report.append(f'DeathCause rows whose causes do not add up to the printed total (as printed in the PDF): {len(mism)}')
    report.extend('  ' + m for m in mism)

    rut = 0
    for sheet in ('DSA_FamilyWelfarePrograms', 'DSA_Vaccines', 'DSA_RegisteredBirths', 'DSA_ReportedDeaths', 'DSA_Anganwadis'):
        grp = defaultdict(dict)
        for r in new_sheet_rows[sheet][1:]:
            if r[1] in NEW_YEARS:
                grp[(r[0], r[1], r[2])][r[3]] = (list(r) + [None] * 12)[4:len(MASTER_HEADERS[sheet])]
        for k, g in grp.items():
            for a, b, t in zip(g.get('Rural', []), g.get('Urban', []), g.get('Total', [])):
                if None not in (a, b, t) and a + b != t:
                    rut += 1
    report.append(f'Rural + Urban != Total cells in new rows (as printed in the PDF): {rut}')

    report.append('')
    report.append('Review_Flags kept as printed (possible reprints / printed zeros / merged figures):')
    for f in flags:
        if f[4] in ('Possible repeat of previous year', 'Printed zeros') or (
                f[4] == 'Layout differs from reference' and 'ONE merged figure' in str(f[5])):
            report.append(f'  {f[0]} {f[1]} {f[2]} | {f[4]} | {str(f[5])[:160]}')

    report.append('')
    report.append('VERIFICATION: ' + ('PASSED' if not errors else f'FAILED ({len(errors)} problems)'))
    report.extend('  ERROR ' + e for e in errors[:200])
    return errors, report


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--master', default=MASTER_PATH, help='pre-merge MH_health.xlsx')
    parser.add_argument('--out', required=True, help='where to write (or, with --verify-only, the file to check)')
    parser.add_argument('--verify-only', action='store_true')
    parser.add_argument('--report', help='also write the verification report to this file')
    args = parser.parse_args()

    if os.path.abspath(args.master) == os.path.abspath(args.out):
        sys.exit('--out must differ from --master: write elsewhere, verify, then replace.')
    try:
        if not args.verify_only:
            write_merged(args.master, args.out)
        errors, report = verify(args.master, args.out)
    except MergeError as e:
        sys.exit(f'ERROR: {e}')
    text = '\n'.join(report)
    print(text)
    if args.report:
        with open(args.report, 'w', encoding='utf-8') as f:
            f.write(text + '\n')
    sys.exit(1 if errors else 0)


if __name__ == '__main__':
    main()
