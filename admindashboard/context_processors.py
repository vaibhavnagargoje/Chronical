from home.models import State, District
from culture.models import CulturalChapter
from statistic.models import StatisticalChapter
from django.contrib.auth.models import User
from footersection.models import Message
from editor.models import SuggestEdit, IntroductionEdit
from sidepanal.models import SidePanelTerm


def dashboard_context(request):
    """
    Context processor to provide common dashboard data to all templates
    """
    if request.user.is_authenticated and request.user.is_staff:
        return {
            'total_states': State.objects.count(),
            'total_districts': District.objects.count(),
            'total_cultural_chapters': CulturalChapter.objects.count(),
            'total_statistical_chapters': StatisticalChapter.objects.count(),
            'total_chapters': CulturalChapter.objects.count() + StatisticalChapter.objects.count(),
            'total_users': User.objects.count(),
            'pending_edit_requests': SuggestEdit.objects.filter(status='pending').count() + IntroductionEdit.objects.filter(status='pending').count(),
            'total_comments': Message.objects.count(),  # Placeholder for future implementation
            'total_sidepanel_terms': SidePanelTerm.objects.count(),
        }
    return {}
