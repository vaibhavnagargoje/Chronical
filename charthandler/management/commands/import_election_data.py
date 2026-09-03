"""
Management command to import election CSV data into the database.

Usage:
    python manage.py import_election_data [--data-dir PATH] [--clear]

Default data directory: Election/ in the project root.

CSV files expected (exported from Election/Original Data):
    LokSabha_Election_Winners.csv
    LokSabha_NOTA_Results.csv
    VidhanSabha_Election_Winners.csv
    VidhanSabha_NOTA_Results.csv

Note:
    VidhanSabha_Election_Results_minus_poll_num.csv is also extracted,
    but is not imported by this command because no separate model is mapped to it.
"""

import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from charthandler.models import (
    LokSabhaElectionWinners,
    LokSabhaNOTAResults,
    VidhanSabhaElectionWinners,
    VidhanSabhaNOTAResults,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _safe_float(value):
    """Safely convert a value to float, returning None for empty/invalid."""
    if value is None:
        return None
    text = str(value).strip()
    if text in ("", "nan", "NaN", "None"):
        return None
    try:
        return float(text.replace(",", ""))
    except (ValueError, TypeError):
        return None


def _safe_int(value):
    """Safely convert a value to int via float, returning None when invalid."""
    parsed = _safe_float(value)
    if parsed is None:
        return None
    return int(parsed)


def _safe_bool(value):
    """Safely convert common truthy/falsey text and numeric values to bool."""
    if value is None:
        return None

    text = str(value).strip().lower()
    if text in ("", "none", "nan"):
        return None

    if text in ("true", "t", "yes", "y", "1"):
        return True
    if text in ("false", "f", "no", "n", "0"):
        return False

    numeric = _safe_float(value)
    if numeric is None:
        return None
    return bool(int(numeric))


def _str(row, col):
    """Get a stripped string from CSV row with empty-string fallback."""
    return str(row.get(col, "") or "").strip()


# ---------------------------------------------------------------------------
# Command
# ---------------------------------------------------------------------------

class Command(BaseCommand):
    help = "Import election CSV data into charthandler election models"

    ALL_MODELS = [
        VidhanSabhaElectionWinners,
        VidhanSabhaNOTAResults,
        LokSabhaElectionWinners,
        LokSabhaNOTAResults,
    ]

    def add_arguments(self, parser):
        parser.add_argument(
            "--data-dir",
            type=str,
            default=os.path.join(settings.BASE_DIR, "Election"),
            help="Path to directory containing election CSV files (default: Election/)",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear all existing election data before importing",
        )

    def handle(self, *args, **options):
        data_dir = options["data_dir"]

        if not os.path.exists(data_dir):
            raise CommandError(f"Data directory not found: {data_dir}")

        self.stdout.write(f"Importing election data from: {data_dir}\n")

        if options["clear"]:
            self.stdout.write("Clearing existing election data...")
            for model_class in self.ALL_MODELS:
                deleted, _ = model_class.objects.all().delete()
                self.stdout.write(f"  Cleared {deleted:>6} rows from {model_class.__name__}")
            self.stdout.write(self.style.SUCCESS("All election data cleared.\n"))

        csv_importers = [
            ("LokSabha_Election_Winners.csv", self._import_lok_sabha_winners),
            ("LokSabha_NOTA_Results.csv", self._import_lok_sabha_nota),
            ("VidhanSabha_Election_Winners.csv", self._import_vidhan_sabha_winners),
            ("VidhanSabha_NOTA_Results.csv", self._import_vidhan_sabha_nota),
        ]

        total_records = 0
        for filename, importer in csv_importers:
            filepath = os.path.join(data_dir, filename)
            if not os.path.exists(filepath):
                self.stdout.write(self.style.WARNING(f"  [SKIP] {filename} - file not found"))
                continue

            try:
                count = importer(filepath)
                total_records += count
                self.stdout.write(self.style.SUCCESS(f"  [OK]   {filename} - {count} records"))
            except Exception as exc:
                self.stdout.write(self.style.ERROR(f"  [ERROR] {filename}: {exc}"))

        self.stdout.write(self.style.SUCCESS(f"\nImport complete! Total records imported: {total_records}"))

    # -----------------------------------------------------------------------
    # Importers
    # -----------------------------------------------------------------------

    def _import_vidhan_sabha_winners(self, filepath):
        records = []
        with open(filepath, "r", encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get("Year"))
                assembly_no = _safe_int(row.get("Assembly No"))
                constituency_no = _safe_int(row.get("Constituency No"))
                candidate = _str(row, "Candidate")

                if not all([year is not None, assembly_no is not None, constituency_no is not None, candidate]):
                    continue

                records.append(VidhanSabhaElectionWinners(
                    assembly_no=assembly_no,
                    constituency_no=constituency_no,
                    year=year,
                    month=_safe_int(row.get("month")),
                    delim_id=_safe_int(row.get("DelimID")),
                    poll_no=_safe_int(row.get("Poll No")),
                    position=_safe_int(row.get("Position")),
                    candidate=candidate,
                    sex=_str(row, "Sex") or None,
                    party=_str(row, "Party"),
                    votes=_safe_float(row.get("Votes")),
                    age_of_winner=_safe_float(row.get("Age of Winner")),
                    average_age_of_contestants=_safe_float(row.get("Average Age of Contestants")),
                    candidate_type=_str(row, "Candidate Type") or None,
                    no_of_valid_votes_casted=_safe_float(row.get("No. of Valid Votes Casted")),
                    no_of_registered_electors=_safe_float(row.get("No. of Registered Electors")),
                    select_constituency=_str(row, "Select Constituency"),
                    constituency_type=_str(row, "Constituency Type") or None,
                    district=_str(row, "District"),
                    sub_region=_str(row, "Sub Region") or None,
                    no_of_candidates=_safe_float(row.get("No. of Candidates")),
                    turnout_rate=_safe_float(row.get("Turnout Rate")),
                    vote_share=_safe_float(row.get("Vote Share")),
                    deposit_lost=_str(row, "Deposit Lost") or None,
                    winning_margin=_safe_float(row.get("Winning Margin")),
                    winning_margin_percentage=_safe_float(row.get("Winning Margin Percentage")),
                    enop=_safe_float(row.get("ENOP")),
                    pid=_str(row, "pid") or None,
                    party_type_tcpd=_str(row, "Party Type TCPD") or None,
                    party_id=_safe_int(row.get("Party ID")),
                    last_poll=_safe_bool(row.get("last poll")),
                    no_of_terms_held_by_winner=_safe_float(row.get("No. of Terms Held by Winner")),
                    last_party=_str(row, "Last Party") or None,
                    last_party_id=_safe_int(row.get("Last Party ID")),
                    last_constituency_name=_str(row, "Last Constituency Name") or None,
                    same_constituency=_safe_bool(row.get("Same Constituency")),
                    same_party=_safe_bool(row.get("Same Party")),
                    no_terms=_safe_float(row.get("No Terms")),
                    turncoat=_safe_bool(row.get("Turncoat")),
                    no_of_turncoat_candidates=_safe_float(row.get("No. of Turncoat Candidates")),
                    pct_of_candidates_turncoat=_safe_float(row.get("% of Candidates Turncoat")),
                    incumbent=_safe_bool(row.get("Incumbent")),
                    recontest=_safe_bool(row.get("Recontest")),
                    no_of_recontesting_candidates=_safe_float(row.get("No. of Recontesting Candidates")),
                    pct_of_candidates_recontesting=_safe_float(row.get("% of Candidates Recontesting")),
                    myneta_education=_str(row, "MyNeta education") or None,
                    tcpd_prof_main=_str(row, "TCPD Prof Main") or None,
                    tcpd_prof_main_desc=_str(row, "TCPD Prof Main Desc") or None,
                    tcpd_prof_second=_str(row, "TCPD Prof Second") or None,
                    tcpd_prof_second_desc=_str(row, "TCPD Prof Second Desc") or None,
                ))

        VidhanSabhaElectionWinners.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_vidhan_sabha_nota(self, filepath):
        records = []
        with open(filepath, "r", encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get("Year"))
                assembly_no = _safe_int(row.get("Assembly No"))
                constituency_no = _safe_int(row.get("Constituency No"))
                candidate = _str(row, "Candidate")

                if not all([year is not None, assembly_no is not None, constituency_no is not None, candidate]):
                    continue

                records.append(VidhanSabhaNOTAResults(
                    assembly_no=assembly_no,
                    constituency_no=constituency_no,
                    year=year,
                    month=_safe_int(row.get("month")),
                    delim_id=_safe_int(row.get("DelimID")),
                    poll_no=_safe_int(row.get("Poll No")),
                    position=_safe_int(row.get("Position")),
                    candidate=candidate,
                    sex=_str(row, "Sex") or None,
                    party=_str(row, "Party"),
                    votes=_safe_float(row.get("Votes")),
                    age_of_winner=_safe_float(row.get("Age of Winner")),
                    average_age_of_contestants=_safe_float(row.get("Average Age of Contestants")),
                    candidate_type=_str(row, "Candidate Type") or None,
                    no_of_valid_votes_casted=_safe_float(row.get("No. of Valid Votes Casted")),
                    no_of_electors=_safe_float(row.get("No. of Electors")),
                    select_constituency=_str(row, "Select Constituency"),
                    constituency_type=_str(row, "Constituency Type") or None,
                    district=_str(row, "District"),
                    sub_region=_str(row, "Sub Region") or None,
                    no_of_candidates=_safe_float(row.get("No. of Candidates")),
                    turnout_rate=_safe_float(row.get("Turnout Rate")),
                    vote_share=_safe_float(row.get("Vote Share")),
                    deposit_lost=_str(row, "Deposit Lost") or None,
                    winning_margin=_safe_float(row.get("Winning Margin")),
                    winning_margin_percentage=_safe_float(row.get("Winning Margin Percentage")),
                    enop=_safe_float(row.get("ENOP")),
                    pid=_str(row, "pid") or None,
                    party_type_tcpd=_str(row, "Party Type TCPD") or None,
                    party_id=_safe_int(row.get("Party ID")),
                    last_poll=_safe_bool(row.get("last poll")),
                    no_of_terms_held_by_winner=_safe_float(row.get("No. of Terms Held by Winner")),
                    last_party=_str(row, "Last Party") or None,
                    last_party_id=_safe_int(row.get("Last Party ID")),
                    last_constituency_name=_str(row, "Last Constituency Name") or None,
                    same_constituency=_safe_bool(row.get("Same Constituency")),
                    same_party=_safe_bool(row.get("Same Party")),
                    no_terms=_safe_float(row.get("No Terms")),
                    turncoat=_safe_bool(row.get("Turncoat")),
                    no_of_turncoat=_safe_float(row.get("No. of Turncoat")),
                    pct_of_turncoats=_safe_float(row.get("% of Turncoats")),
                    incumbent=_safe_bool(row.get("Incumbent")),
                    recontest=_safe_bool(row.get("Recontest")),
                    no_of_recontests=_safe_float(row.get("No. of Recontests")),
                    pct_of_recontests=_safe_float(row.get("% of Recontests")),
                    myneta_education=_str(row, "MyNeta education") or None,
                    tcpd_prof_main=_str(row, "TCPD Prof Main") or None,
                    tcpd_prof_main_desc=_str(row, "TCPD Prof Main Desc") or None,
                    tcpd_prof_second=_str(row, "TCPD Prof Second") or None,
                    tcpd_prof_second_desc=_str(row, "TCPD Prof Second Desc") or None,
                ))

        VidhanSabhaNOTAResults.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_lok_sabha_winners(self, filepath):
        records = []
        with open(filepath, "r", encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get("Year"))
                assembly_no = _safe_int(row.get("Assembly No"))
                constituency_no = _safe_int(row.get("Constituency No"))
                candidate = _str(row, "Candidate")

                if not all([year is not None, assembly_no is not None, constituency_no is not None, candidate]):
                    continue

                records.append(LokSabhaElectionWinners(
                    assembly_no=assembly_no,
                    constituency_no=constituency_no,
                    year=year,
                    month=_safe_int(row.get("month")),
                    poll_no=_safe_int(row.get("Poll No")),
                    delim_id=_safe_int(row.get("DelimID")),
                    position=_safe_int(row.get("Position")),
                    candidate=candidate,
                    sex=_str(row, "Sex") or None,
                    party=_str(row, "Party"),
                    votes=_safe_float(row.get("Votes")),
                    candidate_type=_str(row, "Candidate Type") or None,
                    no_of_valid_votes_casted=_safe_float(row.get("No. of Valid Votes Casted")),
                    no_of_registered_electors=_safe_float(row.get("No. of Registered Electors")),
                    select_constituency=_str(row, "Select Constituency"),
                    district=_str(row, "District"),
                    constituency_type=_str(row, "Constituency Type") or None,
                    sub_region=_str(row, "Sub Region") or None,
                    no_of_candidates=_safe_float(row.get("No. of Candidates")),
                    turnout_rate=_safe_float(row.get("Turnout Rate")),
                    vote_share=_safe_float(row.get("Vote Share")),
                    deposit_lost=_str(row, "Deposit Lost") or None,
                    winning_margin=_safe_float(row.get("Winning Margin")),
                    winning_margin_percentage=_safe_float(row.get("Winning Margin Percentage")),
                    enop=_safe_float(row.get("ENOP")),
                    pid=_str(row, "pid") or None,
                    party_type_tcpd=_str(row, "Party Type TCPD") or None,
                    party_id=_safe_int(row.get("Party ID")),
                    last_poll=_safe_bool(row.get("last poll")),
                    contested=_safe_bool(row.get("Contested")),
                    last_party=_str(row, "Last Party") or None,
                    last_party_id=_safe_int(row.get("Last Party ID")),
                    last_constituency_name=_str(row, "Last Constituency Name") or None,
                    same_constituency=_safe_bool(row.get("Same Constituency")),
                    same_party=_safe_bool(row.get("Same Party")),
                    no_of_terms_held_by_winner=_safe_float(row.get("No. of Terms Held by Winner")),
                    turncoat=_safe_bool(row.get("Turncoat")),
                    no_of_turncoat_candidates=_safe_float(row.get("No. of Turncoat Candidates")),
                    pct_of_candidates_turncoat=_safe_float(row.get("% of Candidates Turncoat")),
                    incumbent=_safe_bool(row.get("Incumbent")),
                    recontest=_safe_bool(row.get("Recontest")),
                    no_of_recontesting_candidates=_safe_float(row.get("No. of Recontesting Candidates")),
                    pct_of_candidates_recontesting=_safe_float(row.get("% of Candidates Recontesting")),
                    myneta_education=_str(row, "MyNeta education") or None,
                    tcpd_prof_main=_str(row, "TCPD Prof Main") or None,
                    tcpd_prof_main_desc=_str(row, "TCPD Prof Main Desc") or None,
                    tcpd_prof_second=_str(row, "TCPD Prof Second") or None,
                    tcpd_prof_second_desc=_str(row, "TCPD Prof Second Desc") or None,
                ))

        LokSabhaElectionWinners.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_lok_sabha_nota(self, filepath):
        records = []
        with open(filepath, "r", encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get("Year"))
                assembly_no = _safe_int(row.get("Assembly No"))
                constituency_no = _safe_int(row.get("Constituency No"))
                candidate = _str(row, "Candidate")

                if not all([year is not None, assembly_no is not None, constituency_no is not None, candidate]):
                    continue

                records.append(LokSabhaNOTAResults(
                    assembly_no=assembly_no,
                    constituency_no=constituency_no,
                    year=year,
                    month=_safe_int(row.get("month")),
                    poll_no=_safe_int(row.get("Poll No")),
                    delim_id=_safe_int(row.get("DelimID")),
                    position=_safe_int(row.get("Position")),
                    candidate=candidate,
                    sex=_str(row, "Sex") or None,
                    party=_str(row, "Party"),
                    votes=_safe_float(row.get("Votes")),
                    candidate_type=_str(row, "Candidate Type") or None,
                    valid_votes=_safe_float(row.get("Valid Votes")),
                    electors=_safe_float(row.get("Electors")),
                    select_constituency=_str(row, "Select Constituency"),
                    district=_str(row, "District"),
                    constituency_type=_str(row, "Constituency Type") or None,
                    sub_region=_str(row, "Sub Region") or None,
                    n_cand=_safe_float(row.get("N Cand")),
                    turnout_percentage=_safe_float(row.get("Turnout Percentage")),
                    vote_share=_safe_float(row.get("Vote Share")),
                    deposit_lost=_str(row, "Deposit Lost") or None,
                    margin=_safe_float(row.get("Margin")),
                    margin_percentage=_safe_float(row.get("Margin Percentage")),
                    enop=_safe_float(row.get("ENOP")),
                    pid=_str(row, "pid") or None,
                    party_type_tcpd=_str(row, "Party Type TCPD") or None,
                    party_id=_safe_int(row.get("Party ID")),
                    last_poll=_safe_bool(row.get("last poll")),
                    contested=_safe_bool(row.get("Contested")),
                    last_party=_str(row, "Last Party") or None,
                    last_party_id=_safe_int(row.get("Last Party ID")),
                    last_constituency_name=_str(row, "Last Constituency Name") or None,
                    same_constituency=_safe_bool(row.get("Same Constituency")),
                    same_party=_safe_bool(row.get("Same Party")),
                    no_terms=_safe_float(row.get("No Terms")),
                    turncoat=_safe_bool(row.get("Turncoat")),
                    incumbent=_safe_bool(row.get("Incumbent")),
                    recontest=_safe_bool(row.get("Recontest")),
                    myneta_education=_str(row, "MyNeta education") or None,
                    tcpd_prof_main=_str(row, "TCPD Prof Main") or None,
                    tcpd_prof_main_desc=_str(row, "TCPD Prof Main Desc") or None,
                    tcpd_prof_second=_str(row, "TCPD Prof Second") or None,
                    tcpd_prof_second_desc=_str(row, "TCPD Prof Second Desc") or None,
                ))

        LokSabhaNOTAResults.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)
