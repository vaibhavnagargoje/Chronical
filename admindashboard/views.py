from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Count, Value, CharField
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from home.models import State, District, FinalCheck
from culture.models import CulturalChapter
from statistic.models import StatisticalChapter
from users.models import Profile
from sidepanal.models import SidePanelTerm, ContextualDefinition
from editor.models import SuggestEdit, IntroductionEdit
from django.utils import timezone
from datetime import datetime, timedelta
import json
from collections import OrderedDict
from django.urls import reverse

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
    total_sidepanel_terms = SidePanelTerm.objects.count()
    
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
        'total_sidepanel_terms': total_sidepanel_terms,
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
    type_filter = request.GET.get('type_filter', 'all')
    
    # Prepare combined chapters list
    chapters_list = []
    
    # Get cultural chapters with review status
    cultural_chapters = CulturalChapter.objects.select_related('district', 'district__state').prefetch_related('final_check').all()
    for chapter in cultural_chapters:
        # Get review status from FinalCheck
        final_check = getattr(chapter, 'final_check', None)
        if final_check:
            if final_check.reviewed:
                status = 'reviewed'
                status_display = 'Reviewed'
            
                
            else:
                status = 'pending'
                status_display = 'Pending Review'
        else:
            status = 'draft'
            status_display = 'Draft'
        
        chapters_list.append({
            'id': chapter.id,
            'name': chapter.name,
            'title': chapter.name,
            'description': f"Cultural chapter covering {chapter.name.lower()} of {chapter.district.name}",
            'district': chapter.district,
            'chapter_type': 'cultural',
            'updated_at': chapter.updated_at,
            'status': status,
            'status_display': status_display,
            'model_type': 'cultural',
            'slug': chapter.slug,
            'final_check': final_check,
        })
    
    # Get statistical chapters with review status
    statistical_chapters = StatisticalChapter.objects.select_related('district', 'district__state').prefetch_related('final_check').all()
    for chapter in statistical_chapters:
        # Get review status from FinalCheck
        final_check = getattr(chapter, 'final_check', None)
        if final_check:
            if final_check.reviewed:
                status = 'reviewed'
                status_display = 'Reviewed'
            elif final_check.ready_for_review:
                status = 'pending'
                status_display = 'Pending Review'
            else:
                status = 'draft'
                status_display = 'Draft'
        else:
            status = 'draft'
            status_display = 'Draft'
        
        chapters_list.append({
            'id': chapter.id,
            'name': chapter.name,
            'title': chapter.name,
            'description': f"Statistical data and analysis for {chapter.name.lower()} in {chapter.district.name}",
            'district': chapter.district,
            'chapter_type': 'statistical',
            'updated_at': chapter.updated_at,
            'status': status,
            'status_display': status_display,
            'model_type': 'statistical',
            'slug': chapter.slug,
            'final_check': final_check,
        })
    
    # Apply search filter
    if search_query:
        chapters_list = [
            chapter for chapter in chapters_list
            if (search_query.lower() in chapter['name'].lower() or
                search_query.lower() in chapter['description'].lower() or
                search_query.lower() in chapter['district'].name.lower() or
                search_query.lower() in chapter['district'].state.name.lower())
        ]
    
    # Apply district filter
    if district_filter:
        chapters_list = [
            chapter for chapter in chapters_list
            if chapter['district'].id == int(district_filter)
        ]
    
    # Apply type filter
    if type_filter == 'cultural':
        chapters_list = [chapter for chapter in chapters_list if chapter['chapter_type'] == 'cultural']
    elif type_filter == 'statistical':
        chapters_list = [chapter for chapter in chapters_list if chapter['chapter_type'] == 'statistical']
    
    # Sort by updated_at (newest first)
    chapters_list.sort(key=lambda x: x['updated_at'] or timezone.now(), reverse=True)
    
    # Convert to objects for template compatibility
    class ChapterObject:
        def __init__(self, data):
            for key, value in data.items():
                setattr(self, key, value)
    
    chapters_objects = [ChapterObject(chapter) for chapter in chapters_list]
    
    # Pagination
    paginator = Paginator(chapters_objects, 18)  # Show 18 chapters per page (3x6 grid)
    page_number = request.GET.get('page')
    chapters_paginated = paginator.get_page(page_number)
    
    # Get statistics
    total_cultural_chapters = CulturalChapter.objects.count()
    total_statistical_chapters = StatisticalChapter.objects.count()
    total_chapters = total_cultural_chapters + total_statistical_chapters
    
    # Count pending chapters based on FinalCheck status
    pending_cultural = FinalCheck.objects.filter(
        cultural_chapter__isnull=False,
        ready_for_review=True,
        reviewed=False
    ).count()
    
    pending_statistical = FinalCheck.objects.filter(
        statistical_chapter__isnull=False,
        ready_for_review=True,
        reviewed=False
    ).count()
    
    pending_chapters = pending_cultural + pending_statistical
    
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
    tab_filter = request.GET.get('tab', 'all')
    
    # Base queryset with profile information
    users_list = User.objects.select_related('profile').all()
    
    # Apply search filter
    if search_query:
        users_list = users_list.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    # Apply tab filter
    if tab_filter == 'admin':
        users_list = users_list.filter(
            Q(profile__is_admin=True) | 
            Q(profile__is_super_admin=True)
        )
    elif tab_filter == 'regular':
        users_list = users_list.filter(
            profile__is_admin=False,
            profile__is_super_admin=False,
            profile__is_reviewer=False,
            profile__is_content_editor=False,
            is_active=True
        )
    elif tab_filter == 'inactive':
        users_list = users_list.filter(is_active=False)
    
    # Apply role filter
    elif role_filter == 'admin':
        users_list = users_list.filter(
            Q(profile__is_admin=True) | 
            Q(profile__is_super_admin=True)
        )
    elif role_filter == 'user':
        users_list = users_list.filter(
            profile__is_admin=False,
            profile__is_super_admin=False
        )
    
    # Apply status filter
    if status_filter == 'active':
        users_list = users_list.filter(is_active=True)
    elif status_filter == 'inactive':
        users_list = users_list.filter(is_active=False)
    
    # Order by date joined (newest first)
    users_list = users_list.order_by('-date_joined')
    
    # Pagination
    paginator = Paginator(users_list, 25)
    page_number = request.GET.get('page')
    users_paginated = paginator.get_page(page_number)
    
    # Get statistics using custom permissions
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    admin_users = User.objects.filter(
        Q(profile__is_admin=True) | 
        Q(profile__is_super_admin=True)
    ).count()
    regular_users = User.objects.filter(
        profile__is_admin=False,
        profile__is_super_admin=False,
        profile__is_reviewer=False,
        profile__is_content_editor=False,
        is_active=True
    ).count()
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
        'tab_filter': tab_filter,
    }
    
    return render(request, 'admindashboard/users.html', context)

@login_required
@user_passes_test(is_staff_user)
@require_POST
def update_user_permissions(request):
    """Update user permissions via AJAX"""
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        permissions = data.get('permissions', {})
        
        # Check if current user has super admin permission
        if not hasattr(request.user, 'profile') or not request.user.profile.is_super_admin:
            return JsonResponse({'success': False, 'error': 'Insufficient permissions'})
        
        user = get_object_or_404(User, id=user_id)
        profile = user.profile
        
        # Update permissions
        profile.is_admin = permissions.get('is_admin', False)
        profile.is_reviewer = permissions.get('is_reviewer', False)
        profile.is_content_editor = permissions.get('is_content_editor', False)
        
        # Only super admins can modify super admin status
        if request.user.profile.is_super_admin:
            profile.is_super_admin = permissions.get('is_super_admin', False)
        
        # Update Django's is_staff based on custom permissions
        user.is_staff = any([
            profile.is_admin,
            profile.is_super_admin,
            profile.is_reviewer,
            profile.is_content_editor
        ])
        
        profile.save()
        user.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Permissions updated successfully',
            'user_role': profile.get_user_types()
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@user_passes_test(is_staff_user)
@require_POST
def delete_user(request):
    """Delete user via AJAX"""
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        
        # Check if current user has super admin permission
        if not hasattr(request.user, 'profile') or not request.user.profile.is_super_admin:
            return JsonResponse({'success': False, 'error': 'Insufficient permissions'})
        
        user = get_object_or_404(User, id=user_id)
        
        # Prevent deleting super admin users
        if hasattr(user, 'profile') and user.profile.is_super_admin:
            return JsonResponse({'success': False, 'error': 'Cannot delete super admin users'})
        
        # Prevent self-deletion
        if user.id == request.user.id:
            return JsonResponse({'success': False, 'error': 'Cannot delete your own account'})
        
        username = user.username
        user.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'User "{username}" has been deleted successfully'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@user_passes_test(is_staff_user)
def edit_requests(request):
    suggest_edits = SuggestEdit.objects.select_related('user').order_by('-created_at')
    introduction_edits = IntroductionEdit.objects.select_related('user', 'district', 'district__state').order_by('-created_at')
    combined_requests = []

    for edit in suggest_edits:
        submitted_by = (edit.user.get_full_name() or edit.user.username) if edit.user else edit.name
        contact_email = edit.user.email if edit.user and edit.user.email else edit.email
        combined_requests.append({
            'pk': edit.pk,
            'source': 'chapter',
            'title': edit.get_chapter_title(),
            'section': edit.section or 'General',
            'status': edit.status,
            'status_display': edit.get_status_display(),
            'edit_type': edit.edit_type,
            'edit_type_display': edit.get_edit_type_display(),
            'submitted_at': edit.created_at,
            'updated_at': edit.updated_at,
            'submitted_by': submitted_by,
            'email': contact_email,
            'notify_on_review': edit.notify_on_review,
        })

    for edit in introduction_edits:
        submitted_by = (edit.user.get_full_name() or edit.user.username) if edit.user else edit.name
        contact_email = edit.user.email if edit.user and edit.user.email else edit.email
        combined_requests.append({
            'pk': edit.pk,
            'source': 'introduction',
            'title': edit.get_district_name(),
            'section': edit.get_section_display(),
            'status': edit.status,
            'status_display': edit.get_status_display(),
            'edit_type': edit.edit_type,
            'edit_type_display': edit.get_edit_type_display(),
            'submitted_at': edit.created_at,
            'updated_at': edit.updated_at,
            'submitted_by': submitted_by,
            'email': contact_email,
            'notify_on_review': edit.notify_on_review,
        })

    combined_requests = sorted(combined_requests, key=lambda item: item['submitted_at'], reverse=True)
    status_filter = request.GET.get('status', '')
    source_filter = request.GET.get('source', '')
    edit_type_filter = request.GET.get('edit_type', '')
    sort_by = request.GET.get('sort', 'latest')

    filtered_requests = combined_requests
    if status_filter:
        filtered_requests = [item for item in filtered_requests if item['status'] == status_filter]
    if source_filter:
        filtered_requests = [item for item in filtered_requests if item['source'] == source_filter]
    if edit_type_filter:
        filtered_requests = [item for item in filtered_requests if item['edit_type'] == edit_type_filter]

    status_order = {'pending': 0, 'in_review': 1, 'approved': 2, 'rejected': 3}
    if sort_by == 'oldest':
        filtered_requests = sorted(filtered_requests, key=lambda item: item['submitted_at'])
    elif sort_by == 'status':
        filtered_requests = sorted(filtered_requests, key=lambda item: (status_order.get(item['status'], 99), item['submitted_at']))
    elif sort_by == 'recent_update':
        filtered_requests = sorted(filtered_requests, key=lambda item: item['updated_at'] or item['submitted_at'], reverse=True)
    else:
        filtered_requests = sorted(filtered_requests, key=lambda item: item['submitted_at'], reverse=True)

    total_requests = len(combined_requests)
    pending_requests = sum(1 for item in combined_requests if item['status'] == 'pending')
    in_review_requests = sum(1 for item in combined_requests if item['status'] == 'in_review')
    approved_requests = sum(1 for item in combined_requests if item['status'] == 'approved')

    edit_type_options = OrderedDict()
    for value, label in SuggestEdit.EDIT_TYPE_CHOICES + IntroductionEdit.EDIT_TYPE_CHOICES:
        edit_type_options.setdefault(value, label)

    context = {
        'total_requests': total_requests,
        'pending_requests': pending_requests,
        'in_review_requests': in_review_requests,
        'approved_requests': approved_requests,
        'chapter_request_count': suggest_edits.count(),
        'introduction_request_count': introduction_edits.count(),
        'requests_list': filtered_requests,
        'visible_requests': len(filtered_requests),
        'status_filter': status_filter,
        'source_filter': source_filter,
        'edit_type_filter': edit_type_filter,
        'sort_by': sort_by,
        'status_choices': SuggestEdit.STATUS_CHOICES,
        'source_choices': [('chapter', 'Chapter Edits'), ('introduction', 'Introduction Edits')],
        'edit_type_choices': list(edit_type_options.items()),
        'sort_choices': [
            ('latest', 'Newest first'),
            ('oldest', 'Oldest first'),
            ('status', 'Status (Pending → Approved)'),
            ('recent_update', 'Recently updated'),
        ],
    }
    return render(request, 'admindashboard/edit_requests.html', context)

@login_required
@user_passes_test(is_staff_user)
def edit_request_detail(request, source, pk):
    if source not in ('chapter', 'introduction'):
        return redirect('admindashboard:edit_requests')

    model = SuggestEdit if source == 'chapter' else IntroductionEdit
    edit = get_object_or_404(model, pk=pk)
    status_choices = model.STATUS_CHOICES
    status_error = False

    if request.method == 'POST':
        new_status = request.POST.get('status', '')
        if new_status in dict(status_choices):
            edit.status = new_status
            edit.review_notes = request.POST.get('review_notes', '').strip()
            if hasattr(edit, 'reviewed_by'):
                edit.reviewed_by = request.user
            edit.save()
            return redirect(f"{reverse('admindashboard:edit_request_detail', args=[source, pk])}?updated=1")
        else:
            status_error = True
            edit.review_notes = request.POST.get('review_notes', edit.review_notes)

    submitted_by = (edit.user.get_full_name() or edit.user.username) if edit.user else edit.name
    contact_email = edit.user.email if edit.user and edit.user.email else edit.email
    related_object = edit.get_chapter() if source == 'chapter' else edit.district
    detail_title = edit.get_chapter_title() if source == 'chapter' else edit.get_district_name()
    section_display = (edit.section or 'General') if source == 'chapter' else edit.get_section_display()

    context = {
        'edit': edit,
        'source': source,
        'source_label': 'Chapter Edit' if source == 'chapter' else 'Introduction Edit',
        'status_choices': status_choices,
        'status_error': status_error,
        'submitted_by': submitted_by,
        'contact_email': contact_email,
        'related_object': related_object,
        'detail_title': detail_title,
        'section_display': section_display,
        'edit_type_display': edit.get_edit_type_display(),
        'status_display': edit.get_status_display(),
        'supporting_file_url': edit.supporting_file.url if edit.supporting_file else None,
        'updated': request.GET.get('updated'),
    }
    return render(request, 'admindashboard/request_detail.html', context)

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