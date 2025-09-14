from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from sidepanal.models import SidePanelTerm, ContextualDefinition
from culture.models import CulturalChapter
from statistic.models import StatisticalChapter
from home.models import District

def is_staff_user(user):
    """Check if user is staff member"""
    return user.is_staff

@login_required
@user_passes_test(is_staff_user)
def sidepanal_dashboard(request):
    """Dashboard overview for sidepanal management"""
    # Get basic statistics
    total_terms = SidePanelTerm.objects.count()
    total_overrides = ContextualDefinition.objects.count()
    active_overrides = ContextualDefinition.objects.filter(is_active=True).count()
    inactive_overrides = total_overrides - active_overrides
    
    # Get recent activity
    recent_terms = SidePanelTerm.objects.order_by('-id')[:5]
    recent_overrides = ContextualDefinition.objects.select_related('term', 'cultural_chapter', 'statistical_chapter').order_by('-id')[:5]
    
    # Get terms with most overrides
    top_terms = SidePanelTerm.objects.annotate(
        overrides_count=Count('contextual_definitions')
    ).filter(overrides_count__gt=0).order_by('-overrides_count')[:10]
    
    # Get chapter statistics
    cultural_overrides = ContextualDefinition.objects.filter(cultural_chapter__isnull=False).count()
    statistical_overrides = ContextualDefinition.objects.filter(statistical_chapter__isnull=False).count()
    
    # Find terms without overrides
    terms_without_overrides = SidePanelTerm.objects.annotate(
        overrides_count=Count('contextual_definitions')
    ).filter(overrides_count=0).count()
    
    context = {
        'total_terms': total_terms,
        'total_overrides': total_overrides,
        'active_overrides': active_overrides,
        'inactive_overrides': inactive_overrides,
        'cultural_overrides': cultural_overrides,
        'statistical_overrides': statistical_overrides,
        'terms_without_overrides': terms_without_overrides,
        'recent_terms': recent_terms,
        'recent_overrides': recent_overrides,
        'top_terms': top_terms,
    }
    
    return render(request, 'sidepanal/dashboard.html', context)




# Side Panel Management Views
@login_required
@user_passes_test(is_staff_user)
def sidepanel_terms(request):
    """Enhanced Side Panel Terms management view"""
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', 'term')
    
    # Base queryset with annotations
    terms_list = SidePanelTerm.objects.annotate(
        overrides_count=Count('contextual_definitions')
    )
    
    # Apply search filter
    if search_query:
        terms_list = terms_list.filter(
            Q(term__icontains=search_query)
        )
    
    # Apply sorting
    valid_sorts = ['term', '-term', 'overrides_count', '-overrides_count']
    if sort_by in valid_sorts:
        terms_list = terms_list.order_by(sort_by)
    else:
        terms_list = terms_list.order_by('term')
    
    # Statistics
    total_terms = SidePanelTerm.objects.count()
    total_overrides = ContextualDefinition.objects.count()
    active_overrides = ContextualDefinition.objects.filter(is_active=True).count()
    
    context = {
        'terms': terms_list,
        'total_terms': total_terms,
        'total_overrides': total_overrides,
        'active_overrides': active_overrides,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    
    return render(request, 'sidepanal/sidepanel_terms.html', context)

@login_required
@user_passes_test(is_staff_user)
def sidepanel_term_create(request):
    """Create new side panel term"""
    if request.method == 'POST':
        term = request.POST.get('term', '').strip()
        default_definition = request.POST.get('default_definition', '').strip()
        
        if term and default_definition:
            try:
                SidePanelTerm.objects.create(
                    term=term,
                    default_definition=default_definition
                )
                messages.success(request, f'Term "{term}" created successfully!')
                return redirect('sidepanal:sidepanel_terms')
            except Exception as e:
                messages.error(request, f'Error creating term: {str(e)}')
        else:
            messages.error(request, 'Both term and definition are required.')
    
    return render(request, 'sidepanal/sidepanel_term_form.html', {
        'form_title': 'Add New Term',
        'form_action': 'create'
    })

@login_required
@user_passes_test(is_staff_user)
def sidepanel_term_edit(request, term_id):
    """Edit side panel term"""
    term = get_object_or_404(SidePanelTerm, id=term_id)
    
    if request.method == 'POST':
        term_text = request.POST.get('term', '').strip()
        default_definition = request.POST.get('default_definition', '').strip()
        
        if term_text and default_definition:
            try:
                term.term = term_text
                term.default_definition = default_definition
                term.save()
                messages.success(request, f'Term "{term.term}" updated successfully!')
                return redirect('sidepanal:sidepanel_terms')
            except Exception as e:
                messages.error(request, f'Error updating term: {str(e)}')
        else:
            messages.error(request, 'Both term and definition are required.')
    
    context = {
        'term': term,
        'form_title': 'Edit Term',
        'form_action': 'edit'
    }
    
    return render(request, 'sidepanal/sidepanel_term_form.html', context)

@login_required
@user_passes_test(is_staff_user)
def sidepanel_term_detail(request, term_id):
    """View side panel term details with contextual overrides"""
    term = get_object_or_404(SidePanelTerm, id=term_id)
    
    # Get all contextual definitions for this term
    contextual_definitions = ContextualDefinition.objects.filter(term=term).select_related(
        'cultural_chapter__district__state',
        'statistical_chapter__district__state'
    ).order_by('-is_active', 'cultural_chapter__name', 'statistical_chapter__name')
    
    # Pagination for overrides
    paginator = Paginator(contextual_definitions, 10)
    page_number = request.GET.get('page')
    overrides_paginated = paginator.get_page(page_number)
    
    context = {
        'term': term,
        'overrides': overrides_paginated,
        'total_overrides': contextual_definitions.count(),
        'active_overrides': contextual_definitions.filter(is_active=True).count(),
    }
    
    return render(request, 'sidepanal/sidepanel_term_detail.html', context)

@login_required
@user_passes_test(is_staff_user)
@require_POST
def sidepanel_term_delete(request):
    """Delete side panel term"""
    try:
        term_id = request.POST.get('term_id')
        term = get_object_or_404(SidePanelTerm, id=term_id)
        term_name = term.term
        term.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Term "{term_name}" has been deleted successfully'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@user_passes_test(is_staff_user)
def sidepanel_overrides(request):
    """Contextual overrides management view"""
    search_query = request.GET.get('search', '')
    chapter_type = request.GET.get('chapter_type', 'all')
    status_filter = request.GET.get('status', 'all')
    
    # Base queryset
    overrides_list = ContextualDefinition.objects.select_related(
        'term',
        'cultural_chapter__district__state',
        'statistical_chapter__district__state'
    ).order_by('-is_active', 'term__term')
    
    # Apply filters
    if search_query:
        overrides_list = overrides_list.filter(
            Q(term__term__icontains=search_query) |
            Q(cultural_chapter__name__icontains=search_query) |
            Q(statistical_chapter__name__icontains=search_query)
        )
    
    if chapter_type == 'cultural':
        overrides_list = overrides_list.filter(cultural_chapter__isnull=False)
    elif chapter_type == 'statistical':
        overrides_list = overrides_list.filter(statistical_chapter__isnull=False)
    
    if status_filter == 'active':
        overrides_list = overrides_list.filter(is_active=True)
    elif status_filter == 'inactive':
        overrides_list = overrides_list.filter(is_active=False)
    
    # Pagination
    paginator = Paginator(overrides_list, 20)
    page_number = request.GET.get('page')
    overrides_paginated = paginator.get_page(page_number)
    
    # Statistics
    total_overrides = ContextualDefinition.objects.count()
    active_overrides = ContextualDefinition.objects.filter(is_active=True).count()
    cultural_overrides = ContextualDefinition.objects.filter(cultural_chapter__isnull=False).count()
    statistical_overrides = ContextualDefinition.objects.filter(statistical_chapter__isnull=False).count()
    
    context = {
        'overrides': overrides_paginated,
        'total_overrides': total_overrides,
        'active_overrides': active_overrides,
        'cultural_overrides': cultural_overrides,
        'statistical_overrides': statistical_overrides,
        'search_query': search_query,
        'chapter_type': chapter_type,
        'status_filter': status_filter,
    }
    
    return render(request, 'sidepanal/sidepanel_overrides.html', context)

@login_required
@user_passes_test(is_staff_user)
def sidepanel_override_create(request):
    """Create new contextual override"""
    if request.method == 'POST':
        term_id = request.POST.get('term_id')
        cultural_chapter_id = request.POST.get('cultural_chapter_id')
        statistical_chapter_id = request.POST.get('statistical_chapter_id')
        override_definition = request.POST.get('override_definition', '').strip()
        is_active = request.POST.get('is_active') == 'on'
        
        # Validation
        if not term_id:
            messages.error(request, 'Please select a term.')
        elif not cultural_chapter_id and not statistical_chapter_id:
            messages.error(request, 'Please select either a cultural or statistical chapter.')
        elif cultural_chapter_id and statistical_chapter_id:
            messages.error(request, 'Please select only one chapter type.')
        else:
            try:
                term = get_object_or_404(SidePanelTerm, id=term_id)
                
                override_data = {
                    'term': term,
                    'override_definition': override_definition,
                    'is_active': is_active,
                }
                
                if cultural_chapter_id:
                    cultural_chapter = get_object_or_404(CulturalChapter, id=cultural_chapter_id)
                    override_data['cultural_chapter'] = cultural_chapter
                else:
                    statistical_chapter = get_object_or_404(StatisticalChapter, id=statistical_chapter_id)
                    override_data['statistical_chapter'] = statistical_chapter
                
                ContextualDefinition.objects.create(**override_data)
                messages.success(request, 'Contextual override created successfully!')
                return redirect('sidepanal:sidepanel_overrides')
                
            except Exception as e:
                messages.error(request, f'Error creating override: {str(e)}')
    
    # Get data for form
    terms = SidePanelTerm.objects.all().order_by('term')
    districts = District.objects.select_related('state').order_by('state__name', 'name')
    
    context = {
        'terms': terms,
        'districts': districts,
        'form_title': 'Add New Override',
        'form_action': 'create'
    }
    
    return render(request, 'sidepanal/sidepanel_override_form.html', context)

@login_required
@user_passes_test(is_staff_user)
def sidepanel_override_edit(request, override_id):
    """Edit contextual override"""
    override = get_object_or_404(ContextualDefinition, id=override_id)
    
    if request.method == 'POST':
        override_definition = request.POST.get('override_definition', '').strip()
        is_active = request.POST.get('is_active') == 'on'
        
        try:
            override.override_definition = override_definition
            override.is_active = is_active
            override.save()
            messages.success(request, 'Contextual override updated successfully!')
            return redirect('sidepanal:sidepanel_overrides')
            
        except Exception as e:
            messages.error(request, f'Error updating override: {str(e)}')
    
    context = {
        'override': override,
        'form_title': 'Edit Override',
        'form_action': 'edit'
    }
    
    return render(request, 'sidepanal/sidepanel_override_form.html', context)

@login_required
@user_passes_test(is_staff_user)
def sidepanel_override_detail(request, override_id):
    """View contextual override details"""
    override = get_object_or_404(ContextualDefinition, id=override_id)
    
    # Get related information
    related_overrides = ContextualDefinition.objects.filter(
        term=override.term
    ).exclude(id=override.id)[:5]
    
    context = {
        'override': override,
        'related_overrides': related_overrides,
        'chapter_name': override.cultural_chapter.name if override.cultural_chapter else override.statistical_chapter.name,
        'chapter_type': 'Cultural' if override.cultural_chapter else 'Statistical',
    }
    
    return render(request, 'sidepanal/sidepanel_override_detail.html', context)

@login_required
@user_passes_test(is_staff_user)
@require_POST
def sidepanel_override_delete(request):
    """Delete contextual override"""
    try:
        override_id = request.POST.get('override_id')
        override = get_object_or_404(ContextualDefinition, id=override_id)
        chapter = override.cultural_chapter or override.statistical_chapter
        term_name = override.term.term
        
        override.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Override for "{term_name}" in chapter "{chapter}" has been deleted successfully'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@user_passes_test(is_staff_user)
def export_overrides(request):
    """Export overrides to CSV"""
    import csv
    from django.http import HttpResponse
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="overrides_export.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Term', 'Chapter', 'Chapter Type', 'District', 'State', 'Override Definition', 'Original Definition', 'Status'])
    
    overrides = ContextualDefinition.objects.select_related('term', 'cultural_chapter', 'statistical_chapter').all()
    
    for override in overrides:
        chapter = override.cultural_chapter or override.statistical_chapter
        chapter_type = 'Cultural' if override.cultural_chapter else 'Statistical'
        
        writer.writerow([
            override.term.term,
            chapter.name,
            chapter_type,
            chapter.district.name,
            chapter.district.state.name,
            override.override_definition or '',
            override.term.default_definition,
            'Active' if override.is_active else 'Inactive'
        ])
    
    return response

@login_required
@user_passes_test(is_staff_user)
def get_chapters_by_district(request):
    """AJAX endpoint to get chapters by district and type"""
    district_id = request.GET.get('district_id')
    chapter_type = request.GET.get('type')  # 'cultural' or 'statistical'
    
    if not district_id or not chapter_type:
        return JsonResponse({'chapters': []})
    
    try:
        district = District.objects.get(id=district_id)
        chapters = []
        
        if chapter_type == 'cultural':
            cultural_chapters = CulturalChapter.objects.filter(district=district).order_by('name')
            chapters = [{'id': chapter.id, 'name': chapter.name} for chapter in cultural_chapters]
        elif chapter_type == 'statistical':
            statistical_chapters = StatisticalChapter.objects.filter(district=district).order_by('name')
            chapters = [{'id': chapter.id, 'name': chapter.name} for chapter in statistical_chapters]
        
        return JsonResponse({'chapters': chapters})
    
    except District.DoesNotExist:
        return JsonResponse({'chapters': []})

@login_required
@user_passes_test(is_staff_user)
def import_terms_bulk(request):
    """Bulk import terms from CSV file"""
    if request.method == 'POST':
        import csv
        import io
        
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return JsonResponse({'success': False, 'error': 'No file uploaded'})
        
        if not uploaded_file.name.endswith('.csv'):
            return JsonResponse({'success': False, 'error': 'Please upload a CSV file'})
        
        try:
            # Read file content
            file_content = uploaded_file.read().decode('utf-8-sig')  # Handle BOM
            csv_data = csv.reader(io.StringIO(file_content))
            
            created_count = 0
            updated_count = 0
            error_count = 0
            errors = []
            
            # Skip header row
            next(csv_data, None)
            
            for row_num, row in enumerate(csv_data, start=2):
                try:
                    if len(row) < 2:
                        errors.append(f"Row {row_num}: Missing required columns")
                        error_count += 1
                        continue
                    
                    term_text = row[0].strip()
                    definition = row[1].strip()
                    
                    if not term_text or not definition:
                        errors.append(f"Row {row_num}: Term and definition are required")
                        error_count += 1
                        continue
                    
                    # Check if term already exists
                    existing_term = SidePanelTerm.objects.filter(term__iexact=term_text).first()
                    
                    if existing_term:
                        # Update existing term
                        existing_term.default_definition = definition
                        existing_term.save()
                        updated_count += 1
                    else:
                        # Create new term
                        SidePanelTerm.objects.create(
                            term=term_text,
                            default_definition=definition
                        )
                        created_count += 1
                        
                except Exception as e:
                    errors.append(f"Row {row_num}: {str(e)}")
                    error_count += 1
            
            # Prepare response
            message = f"Import completed! Created: {created_count}, Updated: {updated_count}"
            if error_count > 0:
                message += f", Errors: {error_count}"
            
            return JsonResponse({
                'success': True,
                'message': message,
                'created': created_count,
                'updated': updated_count,
                'errors': error_count,
                'error_details': errors[:10]  # Return first 10 errors
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'File processing error: {str(e)}'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@user_passes_test(is_staff_user)
def export_terms(request):
    """Export terms to CSV"""
    import csv
    from django.http import HttpResponse
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="terms_export.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Term', 'Definition', 'Overrides Count', 'ID'])
    
    terms = SidePanelTerm.objects.annotate(
        overrides_count=Count('contextual_definitions')
    ).order_by('term')
    
    for term in terms:
        writer.writerow([
            term.term,
            term.default_definition,
            term.overrides_count,
            term.id
        ])
    
    return response
