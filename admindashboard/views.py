from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q, Count, Value, CharField
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from home.models import State, District
from culture.models import CulturalChapter
from statistic.models import StatisticalChapter
from django.utils import timezone
from datetime import datetime, timedelta

# Helper function to check if user is staff
def is_staff_user(user):
    return user.is_staff

# Create your views here.

@login_required
@user_passes_test(is_staff_user)
def dashboard(request):
    """Dashboard view with overview statistics"""
    # Fetch counts for dashboard
    total_states = State.objects.count()
    total_districts = District.objects.count()
    total_cultural_chapters = CulturalChapter.objects.count()
    total_statistical_chapters = StatisticalChapter.objects.count()
    total_chapters = total_cultural_chapters + total_statistical_chapters
    total_users = User.objects.count()
    
    # Get recent activities (latest districts and chapters)
    recent_districts = District.objects.select_related('state').order_by('-id')[:5]
    recent_cultural_chapters = CulturalChapter.objects.select_related('district', 'district__state').order_by('-updated_at')[:3]
    recent_statistical_chapters = StatisticalChapter.objects.select_related('district', 'district__state').order_by('-updated_at')[:3]
    
    context = {
        'total_states': total_states,
        'total_districts': total_districts,
        'total_chapters': total_chapters,
        'total_cultural_chapters': total_cultural_chapters,
        'total_statistical_chapters': total_statistical_chapters,
        'total_users': total_users,
        'recent_districts': recent_districts,
        'recent_cultural_chapters': recent_cultural_chapters,
        'recent_statistical_chapters': recent_statistical_chapters,
        'pending_edit_requests': 0,  # Placeholder for future implementation
        'total_comments': 0,  # Placeholder for future implementation
    }
    
    return render(request, 'admindashboard/dashboard.html', context)

@login_required
@user_passes_test(is_staff_user)
def districts(request):
    """Districts management view"""
    # Get search and filter parameters
    search_query = request.GET.get('search', '')
    state_filter = request.GET.get('state_filter', '')
    status_filter = request.GET.get('status_filter', '')
    
    # Base queryset
    districts_list = District.objects.select_related('state').annotate(
        cultural_chapters_count=Count('culturalchapter'),
        statistical_chapters_count=Count('statisticalchapter')
    )
    
    # Apply search filter
    if search_query:
        districts_list = districts_list.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(state__name__icontains=search_query)
        )
    
    # Apply state filter
    if state_filter:
        districts_list = districts_list.filter(state_id=state_filter)
    
    # Apply status filter (placeholder - assuming all are active for now)
    if status_filter == 'active':
        pass  # All districts are considered active
    elif status_filter == 'pending':
        districts_list = districts_list.none()  # No pending districts for now
    
    # Pagination
    paginator = Paginator(districts_list, 20)  # Show 20 districts per page
    page_number = request.GET.get('page')
    districts_paginated = paginator.get_page(page_number)
    
    # Get statistics
    total_states = State.objects.count()
    total_districts = District.objects.count()
    districts_with_chapters = District.objects.annotate(
        chapter_count=Count('culturalchapter') + Count('statisticalchapter')
    ).filter(chapter_count__gt=0).count()
    pending_districts = 0  # Placeholder
    
    # Get all states for filter dropdown
    states = State.objects.all().order_by('name')
    
    context = {
        'districts': districts_paginated,
        'total_districts': total_districts,
        'total_states': total_states,
        'districts_with_chapters': districts_with_chapters,
        'pending_districts': pending_districts,
        'states': states,
        'search_query': search_query,
        'state_filter': state_filter,
        'status_filter': status_filter,
    }
    
    return render(request, 'admindashboard/districts.html', context)

@login_required
@user_passes_test(is_staff_user)
def chapters(request):
    """Chapters management view"""
    # Get search and filter parameters
    search_query = request.GET.get('search', '')
    district_filter = request.GET.get('district_filter', '')
    type_filter = request.GET.get('type_filter', '')
    
    # Combine cultural and statistical chapters (you might want to create a proper unified model)
    cultural_chapters = CulturalChapter.objects.select_related('district', 'district__state').annotate(
        chapter_type=Value('cultural', output_field=CharField())
    )
    statistical_chapters = StatisticalChapter.objects.select_related('district', 'district__state').annotate(
        chapter_type=Value('statistical', output_field=CharField())
    )
    
    # For now, let's work with cultural chapters as primary example
    chapters_list = cultural_chapters
    
    # Apply search filter
    if search_query:
        chapters_list = chapters_list.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(district__name__icontains=search_query)
        )
    
    # Apply district filter
    if district_filter:
        chapters_list = chapters_list.filter(district_id=district_filter)
    
    # Apply type filter
    if type_filter == 'cultural':
        chapters_list = cultural_chapters
    elif type_filter == 'statistical':
        chapters_list = statistical_chapters
    
    # Pagination
    paginator = Paginator(chapters_list, 18)  # Show 18 chapters per page (3x6 grid)
    page_number = request.GET.get('page')
    chapters_paginated = paginator.get_page(page_number)
    
    # Get statistics
    total_cultural_chapters = CulturalChapter.objects.count()
    total_statistical_chapters = StatisticalChapter.objects.count()
    total_chapters = total_cultural_chapters + total_statistical_chapters
    pending_chapters = 0  # Placeholder
    
    # Get all districts for filter dropdown
    districts = District.objects.select_related('state').order_by('state__name', 'name')
    
    context = {
        'chapters': chapters_paginated,
        'total_chapters': total_chapters,
        'total_cultural_chapters': total_cultural_chapters,
        'total_statistical_chapters': total_statistical_chapters,
        'pending_chapters': pending_chapters,
        'districts': districts,
        'search_query': search_query,
        'district_filter': district_filter,
        'type_filter': type_filter,
    }
    
    return render(request, 'admindashboard/chapters.html', context)

@login_required
@user_passes_test(is_staff_user)
def users(request):
    """Users management view"""
    # Get search and filter parameters
    search_query = request.GET.get('search', '')
    role_filter = request.GET.get('role_filter', '')
    status_filter = request.GET.get('status_filter', '')
    
    # Base queryset
    users_list = User.objects.all()
    
    # Apply search filter
    if search_query:
        users_list = users_list.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    # Apply role filter
    if role_filter == 'admin':
        users_list = users_list.filter(is_staff=True)
    elif role_filter == 'user':
        users_list = users_list.filter(is_staff=False)
    
    # Apply status filter
    if status_filter == 'active':
        users_list = users_list.filter(is_active=True)
    elif status_filter == 'inactive':
        users_list = users_list.filter(is_active=False)
    
    # Order by date joined (newest first)
    users_list = users_list.order_by('-date_joined')
    
    # Pagination
    paginator = Paginator(users_list, 25)  # Show 25 users per page
    page_number = request.GET.get('page')
    users_paginated = paginator.get_page(page_number)
    
    # Get statistics
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    admin_users = User.objects.filter(is_staff=True).count()
    regular_users = User.objects.filter(is_staff=False).count()
    inactive_users = User.objects.filter(is_active=False).count()
    
    # Users joined this month
    this_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    new_users_month = User.objects.filter(date_joined__gte=this_month).count()
    
    context = {
        'users': users_paginated,
        'total_users': total_users,
        'active_users': active_users,
        'admin_users': admin_users,
        'regular_users': regular_users,
        'inactive_users': inactive_users,
        'new_users_month': new_users_month,
        'search_query': search_query,
        'role_filter': role_filter,
        'status_filter': status_filter,
    }
    
    return render(request, 'admindashboard/users.html', context)

# Placeholder views for other sections
@login_required
@user_passes_test(is_staff_user)
def edit_requests(request):
    """Edit requests management view"""
    context = {
        'pending_edit_requests': 0,  # Placeholder
    }
    return render(request, 'admindashboard/edit_requests.html', context)

@login_required
@user_passes_test(is_staff_user)
def comments(request):
    """Comments management view"""
    context = {
        'total_comments': 0,  # Placeholder
    }
    return render(request, 'admindashboard/comments.html', context)

@login_required
@user_passes_test(is_staff_user)
def admin_users(request):
    """Admin users management view"""
    return render(request, 'admindashboard/admin_users.html')

@login_required
@user_passes_test(is_staff_user)
def permissions(request):
    """Permissions management view"""
    return render(request, 'admindashboard/permissions.html')

@login_required
@user_passes_test(is_staff_user)
def settings(request):
    """Settings management view"""
    return render(request, 'admindashboard/settings.html')