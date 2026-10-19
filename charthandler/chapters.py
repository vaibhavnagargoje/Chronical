"""
Single source of truth for the 12 statistics chapters on the chart/data side.

Data files live per state:  <BASE_DIR>/<State.name>/<chapter folder>/
e.g. Maharashtra/Health/, and later Kerala/Health/.
"""
import os

from django.conf import settings


DEFAULT_STATE_SLUG = 'maharashtra'
DEFAULT_STATE_FOLDER = 'Maharashtra'


# Maps StatisticalChapter.name → ChartTemplate.chapter_type slug
CHAPTER_NAME_TO_SLUG = {
    'Agriculture': 'agriculture',
    'Demography': 'demography',
    'Education': 'education',
    'Elections': 'elections',
    'Environment': 'environment',
    'Health': 'health',
    'Industry': 'industry',
    'Labor': 'labor',
    'Livestock & Fisheries': 'livestock-fisheries',
    'Police & Judiciary': 'police-judiciary',
    'Revenue & Expenditure': 'revenue-expenditure',
    'Transport & Communication': 'transport-communication',
}


# Maps ChartTemplate.chapter_type → data folder name inside a state folder
CHAPTER_DATA_FOLDERS = {
    'agriculture': 'Agriculture',
    'demography': 'Demography',
    'education': 'Education',
    'elections': 'Election',
    'environment': 'Environment',
    'health': 'Health',
    'industry': 'Industry',
    'labor': 'Labor',
    'livestock-fisheries': 'Livestock',
    'police-judiciary': 'Police',
    'revenue-expenditure': 'Revenue',
    'transport-communication': 'Transport',
}


def get_chapter_data_dir(chapter_type, state=None):
    """
    Return the data directory for a chapter, e.g. <BASE_DIR>/Maharashtra/Health.

    `state` is a home.State instance; when omitted, Maharashtra is assumed.
    """
    state_folder = state.name if state is not None else DEFAULT_STATE_FOLDER
    return os.path.join(settings.BASE_DIR, state_folder, CHAPTER_DATA_FOLDERS[chapter_type])
