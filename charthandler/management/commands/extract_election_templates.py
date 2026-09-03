"""
Management command to create/update Chart Templates for the Elections chapter.
Charts matching:
https://indiandistricts.in/statistics/maharashtra/<district>/local-politics/

Reference mapping:
Election/Original Data/elections_reference_sheet.xlsx (Graph_Index)
"""

from django.core.management.base import BaseCommand
from charthandler.models import ChartTemplate


ELECTION_SOURCE = "Election Commission of India (ECI) and Trivedi Centre for Political Data"


def build_chart_options(
    y_axis_title,
    x_axis_title="Year",
    is_percent=False,
    disable_all_filter1=False,
    disable_all_filter2=False,
    fixed_filters=None,
):
    options = {
        "scales": {
            "x": {"title": {"display": True, "text": x_axis_title}},
            "y": {"beginAtZero": True, "title": {"display": True, "text": y_axis_title}},
        }
    }
    if is_percent:
        options["is_percentage_format"] = True
    if disable_all_filter1:
        options["disable_all_filter1"] = True
    if disable_all_filter2:
        options["disable_all_filter2"] = True
    if fixed_filters:
        options["fixed_filters"] = fixed_filters
    return options


class Command(BaseCommand):
    help = "Creates/Updates Chart Templates for the Elections chapter."

    def handle(self, *args, **options):
        self.stdout.write("Creating Chart Templates for Elections...\n")

        winners_fixed = {"poll_no": 0, "position": 1}
        nota_fixed = {"poll_no": 0, "candidate": "NOTA"}

        templates = [
            # ------------------------------------------------------------------
            # Lok Sabha (General Elections)
            # ------------------------------------------------------------------
            {
                "title": "A. No. of Electors and Votes Casted - Lok Sabha",
                "chapter_type": "elections",
                "chart_type": "bar",
                "data_source_table": "LokSabhaElectionWinners",
                "x_column": "year",
                "y_columns": ["no_of_registered_electors", "no_of_valid_votes_casted"],
                "dataset_config": [
                    {"label": "No. of Registered Electors", "backgroundColor": "#1a4570"},
                    {"label": "No. of Valid Votes Casted", "backgroundColor": "#e9ba5d"},
                ],
                "main_filter_column": "district",
                "filter1_column": "select_constituency",
                "filter2_column": "",
                "show_filters": True,
                "chart_options": build_chart_options(
                    "No. of Votes / Voters",
                    disable_all_filter1=True,
                    fixed_filters=winners_fixed,
                ),
                "description": ELECTION_SOURCE,
                "additional_info": "Graph does not include by-elections.",
                "display_order": 1,
            },
            {
                "title": "B. Turnout Rate - Lok Sabha",
                "chapter_type": "elections",
                "chart_type": "bar",
                "data_source_table": "LokSabhaElectionWinners",
                "x_column": "year",
                "y_columns": ["turnout_rate"],
                "dataset_config": [
                    {"label": "Turnout Rate", "backgroundColor": "#1a4570"},
                ],
                "main_filter_column": "district",
                "filter1_column": "select_constituency",
                "filter2_column": "",
                "show_filters": True,
                "chart_options": build_chart_options(
                    "Turnout Rate",
                    disable_all_filter1=True,
                    is_percent=True,
                    fixed_filters=winners_fixed,
                ),
                "description": ELECTION_SOURCE,
                "additional_info": "Graph does not include by-elections.",
                "display_order": 2,
            },
            {
                "title": "C. No. of Candidates - Lok Sabha",
                "chapter_type": "elections",
                "chart_type": "bar",
                "data_source_table": "LokSabhaElectionWinners",
                "x_column": "year",
                "y_columns": ["no_of_candidates"],
                "dataset_config": [
                    {"label": "No. of Candidates", "backgroundColor": "#1a4570"},
                ],
                "main_filter_column": "district",
                "filter1_column": "select_constituency",
                "filter2_column": "",
                "show_filters": True,
                "chart_options": build_chart_options(
                    "No. of Candidates",
                    disable_all_filter1=True,
                    fixed_filters=winners_fixed,
                ),
                "description": ELECTION_SOURCE,
                "additional_info": "Graph does not include by-elections.",
                "display_order": 3,
            },
            {
                "title": "D. Candidates Recontesting - Lok Sabha",
                "chapter_type": "elections",
                "chart_type": "bar",
                "data_source_table": "LokSabhaElectionWinners",
                "x_column": "year",
                "y_columns": ["no_of_recontesting_candidates"],
                "dataset_config": [
                    {"label": "No. of Recontesting Candidates", "backgroundColor": "#1a4570"},
                ],
                "main_filter_column": "district",
                "filter1_column": "select_constituency",
                "filter2_column": "",
                "show_filters": True,
                "chart_options": build_chart_options(
                    "No. of Candidates",
                    disable_all_filter1=True,
                    fixed_filters=winners_fixed,
                ),
                "description": ELECTION_SOURCE,
                "additional_info": "Graph does not include by-elections.",
                "display_order": 4,
            },
            {
                "title": "E. Candidates Who Switched Parties (Turncoats) - Lok Sabha",
                "chapter_type": "elections",
                "chart_type": "bar",
                "data_source_table": "LokSabhaElectionWinners",
                "x_column": "year",
                "y_columns": ["no_of_turncoat_candidates"],
                "dataset_config": [
                    {"label": "No. of Turncoat Candidates", "backgroundColor": "#1a4570"},
                ],
                "main_filter_column": "district",
                "filter1_column": "select_constituency",
                "filter2_column": "",
                "show_filters": True,
                "chart_options": build_chart_options(
                    "No. of Candidates",
                    disable_all_filter1=True,
                    fixed_filters=winners_fixed,
                ),
                "description": ELECTION_SOURCE,
                "additional_info": "Graph does not include by-elections.",
                "display_order": 5,
            },
            {
                "title": "F. Vote Share of Winner - Lok Sabha",
                "chapter_type": "elections",
                "chart_type": "bar",
                "data_source_table": "LokSabhaElectionWinners",
                "x_column": "year",
                "y_columns": ["vote_share"],
                "dataset_config": [
                    {"label": "Vote Share", "backgroundColor": "#1a4570"},
                ],
                "main_filter_column": "district",
                "filter1_column": "select_constituency",
                "filter2_column": "",
                "show_filters": True,
                "chart_options": build_chart_options(
                    "Vote Share",
                    disable_all_filter1=True,
                    is_percent=True,
                    fixed_filters=winners_fixed,
                ),
                "description": ELECTION_SOURCE,
                "additional_info": "Graph does not include by-elections.",
                "display_order": 6,
            },
            {
                "title": "G. Winning Margin - Lok Sabha",
                "chapter_type": "elections",
                "chart_type": "bar",
                "data_source_table": "LokSabhaElectionWinners",
                "x_column": "year",
                "y_columns": ["winning_margin"],
                "dataset_config": [
                    {"label": "Winning Margin", "backgroundColor": "#1a4570"},
                ],
                "main_filter_column": "district",
                "filter1_column": "select_constituency",
                "filter2_column": "",
                "show_filters": True,
                "chart_options": build_chart_options(
                    "Margin",
                    disable_all_filter1=True,
                    fixed_filters=winners_fixed,
                ),
                "description": ELECTION_SOURCE,
                "additional_info": "Graph does not include by-elections.",
                "display_order": 7,
            },
            {
                "title": "H. Winning Margin Percentage - Lok Sabha",
                "chapter_type": "elections",
                "chart_type": "bar",
                "data_source_table": "LokSabhaElectionWinners",
                "x_column": "year",
                "y_columns": ["winning_margin_percentage"],
                "dataset_config": [
                    {"label": "Winning Margin Percentage", "backgroundColor": "#1a4570"},
                ],
                "main_filter_column": "district",
                "filter1_column": "select_constituency",
                "filter2_column": "",
                "show_filters": True,
                "chart_options": build_chart_options(
                    "Margin (%)",
                    disable_all_filter1=True,
                    is_percent=True,
                    fixed_filters=winners_fixed,
                ),
                "description": ELECTION_SOURCE,
                "additional_info": "Graph does not include by-elections.",
                "display_order": 8,
            },
            {
                "title": "I. Vote Share for NOTA - Lok Sabha",
                "chapter_type": "elections",
                "chart_type": "bar",
                "data_source_table": "LokSabhaNOTAResults",
                "x_column": "year",
                "y_columns": ["vote_share"],
                "dataset_config": [
                    {"label": "Vote Share", "backgroundColor": "#1a4570"},
                ],
                "main_filter_column": "district",
                "filter1_column": "select_constituency",
                "filter2_column": "",
                "show_filters": True,
                "chart_options": build_chart_options(
                    "Vote Share",
                    disable_all_filter1=True,
                    is_percent=True,
                    fixed_filters=nota_fixed,
                ),
                "description": ELECTION_SOURCE,
                "additional_info": "NOTA is short for None of the Above. The option is designed to allow the voter to indicate disapproval of all candidates. Graph does not include by-elections.",
                "display_order": 9,
            },
            {
                "title": "J. Effective Number of Parties (ENOP) - Lok Sabha",
                "chapter_type": "elections",
                "chart_type": "bar",
                "data_source_table": "LokSabhaElectionWinners",
                "x_column": "year",
                "y_columns": ["enop"],
                "dataset_config": [
                    {"label": "ENOP", "backgroundColor": "#1a4570"},
                ],
                "main_filter_column": "district",
                "filter1_column": "select_constituency",
                "filter2_column": "",
                "show_filters": True,
                "chart_options": build_chart_options(
                    "ENOP",
                    disable_all_filter1=True,
                    fixed_filters=winners_fixed,
                ),
                "description": ELECTION_SOURCE,
                "additional_info": "ENOP (Effective Number of Parties) shows how many parties have real influence in an election. It essentially calculates how many equal-sized parties would give the observed competitiveness. Graph does not include by-elections.",
                "display_order": 10,
            },
            {
                "title": "K. No. of Terms Held by Winner - Lok Sabha",
                "chapter_type": "elections",
                "chart_type": "bar",
                "data_source_table": "LokSabhaElectionWinners",
                "x_column": "year",
                "y_columns": ["no_of_terms_held_by_winner"],
                "dataset_config": [
                    {"label": "No. of Terms Held by Winner", "backgroundColor": "#1a4570"},
                ],
                "main_filter_column": "district",
                "filter1_column": "select_constituency",
                "filter2_column": "",
                "show_filters": True,
                "chart_options": build_chart_options(
                    "No. of Terms",
                    disable_all_filter1=True,
                    fixed_filters=winners_fixed,
                ),
                "description": ELECTION_SOURCE,
                "additional_info": "Graph does not include by-elections.",
                "display_order": 11,
            },

            # ------------------------------------------------------------------
            # Vidhan Sabha (Assembly Elections)
            # ------------------------------------------------------------------
            {
                "title": "A. No. of Electors and Votes Casted - Vidhan Sabha",
                "chapter_type": "elections",
                "chart_type": "bar",
                "data_source_table": "VidhanSabhaElectionWinners",
                "x_column": "year",
                "y_columns": ["no_of_registered_electors", "no_of_valid_votes_casted"],
                "dataset_config": [
                    {"label": "No. of Registered Electors", "backgroundColor": "#1a4570"},
                    {"label": "No. of Valid Votes Casted", "backgroundColor": "#e9ba5d"},
                ],
                "main_filter_column": "district",
                "filter1_column": "select_constituency",
                "filter2_column": "",
                "show_filters": True,
                "chart_options": build_chart_options(
                    "No. of Votes / Voters",
                    disable_all_filter1=True,
                    fixed_filters=winners_fixed,
                ),
                "description": ELECTION_SOURCE,
                "additional_info": "Graph does not include by-elections.",
                "display_order": 12,
            },
            {
                "title": "B. Turnout Rate - Vidhan Sabha",
                "chapter_type": "elections",
                "chart_type": "bar",
                "data_source_table": "VidhanSabhaElectionWinners",
                "x_column": "year",
                "y_columns": ["turnout_rate"],
                "dataset_config": [
                    {"label": "Turnout Rate", "backgroundColor": "#1a4570"},
                ],
                "main_filter_column": "district",
                "filter1_column": "select_constituency",
                "filter2_column": "",
                "show_filters": True,
                "chart_options": build_chart_options(
                    "Turnout Rate",
                    disable_all_filter1=True,
                    is_percent=True,
                    fixed_filters=winners_fixed,
                ),
                "description": ELECTION_SOURCE,
                "additional_info": "Graph does not include by-elections.",
                "display_order": 13,
            },
            {
                "title": "C. No. of Candidates - Vidhan Sabha",
                "chapter_type": "elections",
                "chart_type": "bar",
                "data_source_table": "VidhanSabhaElectionWinners",
                "x_column": "year",
                "y_columns": ["no_of_candidates"],
                "dataset_config": [
                    {"label": "No. of Candidates", "backgroundColor": "#1a4570"},
                ],
                "main_filter_column": "district",
                "filter1_column": "select_constituency",
                "filter2_column": "",
                "show_filters": True,
                "chart_options": build_chart_options(
                    "No. of Candidates",
                    disable_all_filter1=True,
                    fixed_filters=winners_fixed,
                ),
                "description": ELECTION_SOURCE,
                "additional_info": "Graph does not include by-elections.",
                "display_order": 14,
            },
            {
                "title": "D. Candidates Recontesting - Vidhan Sabha",
                "chapter_type": "elections",
                "chart_type": "bar",
                "data_source_table": "VidhanSabhaElectionWinners",
                "x_column": "year",
                "y_columns": ["no_of_recontesting_candidates"],
                "dataset_config": [
                    {"label": "No. of Recontesting Candidates", "backgroundColor": "#1a4570"},
                ],
                "main_filter_column": "district",
                "filter1_column": "select_constituency",
                "filter2_column": "",
                "show_filters": True,
                "chart_options": build_chart_options(
                    "No. of Candidates",
                    disable_all_filter1=True,
                    fixed_filters=winners_fixed,
                ),
                "description": ELECTION_SOURCE,
                "additional_info": "Graph does not include by-elections.",
                "display_order": 15,
            },
            {
                "title": "E. Candidates Who Switched Parties (Turncoats) - Vidhan Sabha",
                "chapter_type": "elections",
                "chart_type": "bar",
                "data_source_table": "VidhanSabhaElectionWinners",
                "x_column": "year",
                "y_columns": ["no_of_turncoat_candidates"],
                "dataset_config": [
                    {"label": "No. of Turncoat Candidates", "backgroundColor": "#1a4570"},
                ],
                "main_filter_column": "district",
                "filter1_column": "select_constituency",
                "filter2_column": "",
                "show_filters": True,
                "chart_options": build_chart_options(
                    "No. of Candidates",
                    disable_all_filter1=True,
                    fixed_filters=winners_fixed,
                ),
                "description": ELECTION_SOURCE,
                "additional_info": "Graph does not include by-elections.",
                "display_order": 16,
            },
            {
                "title": "F. Vote Share of Winner - Vidhan Sabha",
                "chapter_type": "elections",
                "chart_type": "bar",
                "data_source_table": "VidhanSabhaElectionWinners",
                "x_column": "year",
                "y_columns": ["vote_share"],
                "dataset_config": [
                    {"label": "Vote Share", "backgroundColor": "#1a4570"},
                ],
                "main_filter_column": "district",
                "filter1_column": "select_constituency",
                "filter2_column": "",
                "show_filters": True,
                "chart_options": build_chart_options(
                    "Vote Share",
                    disable_all_filter1=True,
                    is_percent=True,
                    fixed_filters=winners_fixed,
                ),
                "description": ELECTION_SOURCE,
                "additional_info": "Graph does not include by-elections.",
                "display_order": 17,
            },
            {
                "title": "G. Winning Margin - Vidhan Sabha",
                "chapter_type": "elections",
                "chart_type": "bar",
                "data_source_table": "VidhanSabhaElectionWinners",
                "x_column": "year",
                "y_columns": ["winning_margin"],
                "dataset_config": [
                    {"label": "Winning Margin", "backgroundColor": "#1a4570"},
                ],
                "main_filter_column": "district",
                "filter1_column": "select_constituency",
                "filter2_column": "",
                "show_filters": True,
                "chart_options": build_chart_options(
                    "Margin",
                    disable_all_filter1=True,
                    fixed_filters=winners_fixed,
                ),
                "description": ELECTION_SOURCE,
                "additional_info": "Graph does not include by-elections.",
                "display_order": 18,
            },
            {
                "title": "H. Winning Margin Percentage - Vidhan Sabha",
                "chapter_type": "elections",
                "chart_type": "bar",
                "data_source_table": "VidhanSabhaElectionWinners",
                "x_column": "year",
                "y_columns": ["winning_margin_percentage"],
                "dataset_config": [
                    {"label": "Winning Margin Percentage", "backgroundColor": "#1a4570"},
                ],
                "main_filter_column": "district",
                "filter1_column": "select_constituency",
                "filter2_column": "",
                "show_filters": True,
                "chart_options": build_chart_options(
                    "Margin (%)",
                    disable_all_filter1=True,
                    is_percent=True,
                    fixed_filters=winners_fixed,
                ),
                "description": ELECTION_SOURCE,
                "additional_info": "Graph does not include by-elections.",
                "display_order": 19,
            },
            {
                "title": "I. Vote Share for NOTA - Vidhan Sabha",
                "chapter_type": "elections",
                "chart_type": "bar",
                "data_source_table": "VidhanSabhaNOTAResults",
                "x_column": "year",
                "y_columns": ["vote_share"],
                "dataset_config": [
                    {"label": "Vote Share", "backgroundColor": "#1a4570"},
                ],
                "main_filter_column": "district",
                "filter1_column": "select_constituency",
                "filter2_column": "",
                "show_filters": True,
                "chart_options": build_chart_options(
                    "Vote Share",
                    disable_all_filter1=True,
                    is_percent=True,
                    fixed_filters=nota_fixed,
                ),
                "description": ELECTION_SOURCE,
                "additional_info": "NOTA is short for None of the Above. The option is designed to allow the voter to indicate disapproval of all candidates. Graph does not include by-elections.",
                "display_order": 20,
            },
            {
                "title": "J. Effective Number of Parties (ENOP) - Vidhan Sabha",
                "chapter_type": "elections",
                "chart_type": "bar",
                "data_source_table": "VidhanSabhaElectionWinners",
                "x_column": "year",
                "y_columns": ["enop"],
                "dataset_config": [
                    {"label": "ENOP", "backgroundColor": "#1a4570"},
                ],
                "main_filter_column": "district",
                "filter1_column": "select_constituency",
                "filter2_column": "",
                "show_filters": True,
                "chart_options": build_chart_options(
                    "ENOP",
                    disable_all_filter1=True,
                    fixed_filters=winners_fixed,
                ),
                "description": ELECTION_SOURCE,
                "additional_info": "ENOP (Effective Number of Parties) shows how many parties have real influence in an election. It essentially calculates how many equal-sized parties would give the observed competitiveness. Graph does not include by-elections.",
                "display_order": 21,
            },
            {
                "title": "K. No. of Terms Held by Winner - Vidhan Sabha",
                "chapter_type": "elections",
                "chart_type": "bar",
                "data_source_table": "VidhanSabhaElectionWinners",
                "x_column": "year",
                "y_columns": ["no_of_terms_held_by_winner"],
                "dataset_config": [
                    {"label": "No. of Terms Held by Winner", "backgroundColor": "#1a4570"},
                ],
                "main_filter_column": "district",
                "filter1_column": "select_constituency",
                "filter2_column": "",
                "show_filters": True,
                "chart_options": build_chart_options(
                    "No. of Terms",
                    disable_all_filter1=True,
                    fixed_filters=winners_fixed,
                ),
                "description": ELECTION_SOURCE,
                "additional_info": "Graph does not include by-elections.",
                "display_order": 22,
            },
            {
                "title": "L. Age of Winner vs Average Age of All Contestants - Vidhan Sabha",
                "chapter_type": "elections",
                "chart_type": "bar",
                "data_source_table": "VidhanSabhaElectionWinners",
                "x_column": "year",
                "y_columns": ["age_of_winner", "average_age_of_contestants"],
                "dataset_config": [
                    {"label": "Age of Winner", "backgroundColor": "#1a4570"},
                    {"label": "Average Age of Contestants", "backgroundColor": "#e9ba5d"},
                ],
                "main_filter_column": "district",
                "filter1_column": "select_constituency",
                "filter2_column": "",
                "show_filters": True,
                "chart_options": build_chart_options(
                    "Age",
                    disable_all_filter1=True,
                    fixed_filters=winners_fixed,
                ),
                "description": ELECTION_SOURCE,
                "additional_info": "Graph does not include by-elections.",
                "display_order": 23,
            },
        ]

        count_new = 0
        count_updated = 0

        for config in templates:
            obj, created = ChartTemplate.objects.update_or_create(
                title=config["title"],
                chapter_type=config["chapter_type"],
                defaults=config,
            )
            if created:
                count_new += 1
                self.stdout.write(f"  [NEW] {obj.title}")
            else:
                count_updated += 1
                self.stdout.write(f"  [UPD] {obj.title}")

        expected_titles = {config["title"] for config in templates}
        stale = list(
            ChartTemplate.objects
            .filter(chapter_type="elections")
            .exclude(title__in=expected_titles)
            .values_list("title", flat=True)
        )
        if stale:
            self.stdout.write(self.style.WARNING(
                "\nStale elections templates (not in this command):\n"
                + "\n".join(f"  - {t}" for t in stale)
            ))

        self.stdout.write(self.style.SUCCESS(
            f"\nDone! {len(templates)} templates processed. ({count_new} new, {count_updated} updated)"
        ))
