from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db import transaction
from django.http import Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils import timezone
import json
from django.conf import settings
from .forms import ChapterSelectForm
from .models import SuggestEdit, IntroductionEdit
from django.utils.text import slugify

# Import models from BOTH apps
from culture.models import (
    CulturalChapter, ContentBlock as CulturalContentBlock, HeadingBlockOne as CulturalH1,
    HeadingBlockTwo as CulturalH2, HeadingBlockThree as CulturalH3,
    ParagraphBlock as CulturalP, ImageBlock as CulturalImg, ReferenceBlock as CulturalRef,
    ChartBlock as CulturalChartBlock  # Renamed to avoid conflict
)
from statistic.models import (
    StatisticalChapter, StatisticContentBlock, HeadingBlockOne as StatH1,
    HeadingBlockTwo as StatH2, HeadingBlockThree as StatH3,
    ParagraphBlock as StatP, ImageBlock as StatImg, ReferenceBlock as StatRef,
    ChartBlock as StatChartBlock  # Renamed to avoid conflict
)

# Import review models
from home.models import DeveloperCheck, FinalCheck, District, DistrictQuickFact

# A central configuration to make views generic without rewriting the logic.
APP_CONFIG = {
    'culture': {
        'title': 'Cultural',
        'ChapterModel': CulturalChapter,
        'BaseBlockModel': CulturalContentBlock,
        'BLOCK_TYPE_MAP': {
            'heading1': CulturalH1, 'heading2': CulturalH2, 'heading3': CulturalH3,
            'paragraph': CulturalP, 'image': CulturalImg, 'reference': CulturalRef,
            'chart': CulturalChartBlock  # Updated to use renamed import
        }
    },
    'statistic': {
        'title': 'Statistical',
        'ChapterModel': StatisticalChapter,
        'BaseBlockModel': StatisticContentBlock,
        'BLOCK_TYPE_MAP': {
            'heading1': StatH1, 'heading2': StatH2, 'heading3': StatH3,
            'paragraph': StatP, 'image': StatImg, 'reference': StatRef,
            'chart': StatChartBlock  # Updated to use renamed import
        }
    }
}

def get_app_config(app_label):
    """Helper function to get the config or raise a 404 error."""
    config = APP_CONFIG.get(app_label)
    if not config:
        raise Http404(f"Editor not configured for app: '{app_label}'")
    return config

def reviewer_required(view_func):
    """Decorator to check if user has reviewer permissions"""
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to login page
        
        # Check if user has reviewer or super admin permissions
        if not (hasattr(request.user, 'profile') and request.user.profile.is_reviewer):
            raise PermissionDenied("You don't have permission to access the editor.")
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@login_required
@reviewer_required
def select_chapter_view(request, app_label):
    """View to select a district and chapter, now aware of the app."""
    config = get_app_config(app_label)
    ChapterModel = config['ChapterModel']

    if request.method == 'POST':
        form = ChapterSelectForm(request.POST, app_label=app_label)
        if form.is_valid():
            district = form.cleaned_data['district']
            chapter_name = form.cleaned_data['chapter_name']
            
            chapter, created = ChapterModel.objects.get_or_create(
                district=district,
                name=chapter_name
            )
            return redirect(reverse('editor:chapter_editor', kwargs={'app_label': app_label, 'chapter_id': chapter.id}))
    else:
        form = ChapterSelectForm(app_label=app_label)

    context = {
        'form': form,
        'app_label': app_label,
        'app_title': config['title'],
    }
    return render(request, 'editor/select_chapter.html', context)


@login_required
@reviewer_required
def chapter_editor_view(request, app_label, chapter_id):
    """ The main editor view, now using a config to support both apps."""
    config = get_app_config(app_label)
    ChapterModel = config['ChapterModel']
    BaseBlockModel = config['BaseBlockModel']
    BLOCK_TYPE_MAP = config['BLOCK_TYPE_MAP']

    chapter = get_object_or_404(
        ChapterModel.objects.select_related('district__state'),
        id=chapter_id
    )

    # Get or create review checks
    developer_check = None
    final_check = None
    
    if app_label == 'culture':
        developer_check, _ = DeveloperCheck.objects.get_or_create(
            cultural_chapter=chapter,
            defaults={'created_by': request.user}
        )
        final_check, _ = FinalCheck.objects.get_or_create(
            cultural_chapter=chapter,
            defaults={'created_by': request.user}
        )
    elif app_label == 'statistic':
        developer_check, _ = DeveloperCheck.objects.get_or_create(
            statistical_chapter=chapter,
            defaults={'created_by': request.user}
        )
        final_check, _ = FinalCheck.objects.get_or_create(
            statistical_chapter=chapter,
            defaults={'created_by': request.user}
        )

    if request.method == 'POST':
        content_data_json = request.POST.get('content_data')
        if not content_data_json:
            return redirect(reverse('editor:chapter_editor', kwargs={'app_label': app_label, 'chapter_id': chapter.id}))

        content_data = json.loads(content_data_json)
        
        try:
            with transaction.atomic():
                existing_block_ids = set(chapter.content_blocks.values_list('id', flat=True))
                submitted_block_ids = set()

                order_index = 0  # Initialize the order counter outside the loop
                
                for block_data in content_data:
                    block_id = block_data.pop('id', None)
                    block_type_str = block_data.get('type')
                    
                    # Handle bulk chart upload - process multiple files
                    if block_type_str == 'bulk-chart' and block_data.get('is_bulk_upload'):
                        bulk_file_id = block_data.get('bulk_chart_files_id')
                        title_prefix = block_data.get('title_prefix', '')
                        
                        if bulk_file_id and bulk_file_id in request.FILES:
                            # Get all files with this name (multiple file upload)
                            files = request.FILES.getlist(bulk_file_id)
                            
                            # Sort files by name
                            files.sort(key=lambda f: f.name)
                            
                            # Get the correct ChartBlock class based on app_label
                            ChartBlockClass = CulturalChartBlock if app_label == 'culture' else StatChartBlock
                            
                            # Create a chart block for each file
                            for chart_file in files:
                                # Create a title from prefix and filename
                                file_name = chart_file.name
                                # Remove .html extension for display in title
                                base_name = file_name.rsplit('.', 1)[0] if '.' in file_name else file_name
                                # Create title with prefix (if provided)
                                chart_title = f"{title_prefix} {base_name}" if title_prefix else base_name
                                
                                # Create a new chart block
                                ChartBlockClass.objects.create(
                                    chapter=chapter,
                                    order=order_index,
                                    title=chart_title,
                                    chart_html_file=chart_file
                                )
                                order_index += 1
                        
                        # Skip the rest of the loop for bulk uploads
                        continue
                
                    # Handle existing blocks (unchanged from your original code)
                    if block_id:
                        submitted_block_ids.add(int(block_id))
                        try:
                            block_instance = BaseBlockModel.objects.get(id=block_id, chapter=chapter).get_real_instance()
                            block_instance.order = order_index
                            
                            # Your original block update logic remains unchanged
                            if isinstance(block_instance, (CulturalH1, StatH1, CulturalH2, StatH2, CulturalH3, StatH3)):
                                block_instance.text = block_data.get('text', '')
                            elif isinstance(block_instance, (CulturalP, StatP)):
                                block_instance.content = block_data.get('content', '')
                            elif isinstance(block_instance, (CulturalRef, StatRef)):
                                block_instance.text = block_data.get('text', '')
                                block_instance.link = block_data.get('link', '')
                            elif isinstance(block_instance, (CulturalImg, StatImg)):
                                block_instance.caption = block_data.get('caption', '')
                                block_instance.alt_text = block_data.get('alt_text', '')
                                block_instance.img_ref = block_data.get('img_ref', '')
                                image_file_id = block_data.get('image_id')
                                if image_file_id and request.FILES.get(image_file_id):
                                    block_instance.image = request.FILES[image_file_id]
                            elif isinstance(block_instance, (CulturalChartBlock, StatChartBlock)):  # Updated to use renamed imports
                                block_instance.title = block_data.get('title', '')
                                chart_file_id = block_data.get('chart_file_id')
                                if chart_file_id and request.FILES.get(chart_file_id):
                                    block_instance.chart_html_file = request.FILES[chart_file_id]

                            block_instance.save()
                            order_index += 1
                        except BaseBlockModel.DoesNotExist:
                            continue 
                    
                    # Create new blocks (unchanged from your original code)
                    else:
                        BlockModelClass = BLOCK_TYPE_MAP.get(block_type_str)
                        if not BlockModelClass: continue
                        
                        block_data.pop('type', None)
                        block_data['chapter'] = chapter
                        block_data['order'] = order_index
                        
                        # Your original image block logic, preserved
                        if block_type_str == 'image':
                            image_file_id = block_data.pop('image_id', None)
                            if image_file_id and request.FILES.get(image_file_id):
                                block_data['image'] = request.FILES[image_file_id]
                            else: continue
                        
                        # Logic to create the new ChartBlock
                        elif block_type_str == 'chart':
                            chart_file_id = block_data.pop('chart_file_id', None)
                            if chart_file_id and request.FILES.get(chart_file_id):
                                block_data['chart_html_file'] = request.FILES[chart_file_id]
                            else: continue

                        BlockModelClass.objects.create(**block_data)
                        order_index += 1

                # --- DELETE blocks removed on the frontend ---
                # Unchanged from your original code
                ids_to_delete = existing_block_ids - submitted_block_ids
                if ids_to_delete:
                    for block_id in ids_to_delete:
                        try:
                            BaseBlockModel.objects.get(id=block_id).delete()
                        except BaseBlockModel.DoesNotExist:
                            continue

                # Ensure chapter timestamp reflects editor changes
                if hasattr(chapter, 'updated_at'):
                    ChapterModel.objects.filter(pk=chapter.pk).update(updated_at=timezone.now())
        except Exception as e:
            print(f"Error saving content: {e}") 
            return redirect(reverse('editor:chapter_editor', kwargs={'app_label': app_label, 'chapter_id': chapter.id}))

    # GET request logic using your requested method
    content_blocks = chapter.content_blocks.all().get_real_instances()
    
    context = {
        'chapter': chapter,
        'content_blocks': content_blocks,
        'app_label': app_label,
        'app_title': config['title'],
        'developer_check': developer_check,
        'final_check': final_check,
    }
     # Clean up TinyMCE instances before rendering
    if hasattr(settings, 'TINYMCE_JS_URL'):
        settings.TINYMCE_JS_URL = settings.STATIC_URL + 'tinymce/tinymce.min.js'
    return render(request, 'editor/chapter_editor.html', context)

@login_required
@reviewer_required
def update_review_status(request, app_label, chapter_id):
    """AJAX view to update review status"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Only POST method allowed'})
    
    try:
        config = get_app_config(app_label)
        ChapterModel = config['ChapterModel']
        
        chapter = get_object_or_404(
            ChapterModel.objects.select_related('district__state'),
            id=chapter_id
        )
        
        data = json.loads(request.body)
        check_type = data.get('check_type')
        reviewed = data.get('reviewed', False)
        
        if check_type not in ['developer', 'final']:
            return JsonResponse({'success': False, 'error': 'Invalid check type'})
        
        # Get or create the appropriate check object
        if check_type == 'developer':
            if app_label == 'culture':
                check_obj, _ = DeveloperCheck.objects.get_or_create(
                    cultural_chapter=chapter,
                    defaults={'created_by': request.user}
                )
            else:  # statistic
                check_obj, _ = DeveloperCheck.objects.get_or_create(
                    statistical_chapter=chapter,
                    defaults={'created_by': request.user}
                )
        else:  # final
            if app_label == 'culture':
                check_obj, _ = FinalCheck.objects.get_or_create(
                    cultural_chapter=chapter,
                    defaults={'created_by': request.user}
                )
            else:  # statistic
                check_obj, _ = FinalCheck.objects.get_or_create(
                    statistical_chapter=chapter,
                    defaults={'created_by': request.user}
                )
        
        # Update the review status
        check_obj.reviewed = reviewed
        check_obj.reviewed_by = request.user if reviewed else None
        check_obj.reviewed_at = timezone.now() if reviewed else None
        check_obj.save()
        
        return JsonResponse({
            'success': True,
            'reviewed': reviewed,
            'reviewed_by': request.user.get_full_name() or request.user.username,
            'reviewed_at': check_obj.reviewed_at.isoformat() if check_obj.reviewed_at else None
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def suggest_edit_view(request, app_label, chapter_id):
    """View for suggesting edits to a chapter"""
    config = get_app_config(app_label)
    ChapterModel = config['ChapterModel']
    BaseBlockModel = config['BaseBlockModel']
    
    chapter = get_object_or_404(
        ChapterModel.objects.select_related('district__state'),
        id=chapter_id
    )
    
    if request.method == 'POST':
        # Create suggestion from form data
        suggestion = SuggestEdit(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            user=request.user if request.user.is_authenticated else None,
            app_label=app_label,
            chapter_id=chapter_id,
            section=request.POST.get('section', ''),
            edit_type=request.POST.get('edit_type'),
            current_text=request.POST.get('current_text', ''),
            suggested_text=request.POST.get('suggested_text'),
            reason=request.POST.get('reason'),
            sources=request.POST.get('sources', ''),
            notify_on_review=request.POST.get('notification') == 'on',
        )
        
        # Handle file upload
        if request.FILES.get('file-upload'):
            suggestion.supporting_file = request.FILES['file-upload']
        
        suggestion.save()
        
        messages.success(request, 'Your edit suggestion has been submitted successfully!')
        return redirect(chapter.get_absolute_url())
    
    # Get content blocks for this chapter and generate section options dynamically
    content_blocks = chapter.content_blocks.all().get_real_instances()
    
    # Generate section options from HeadingBlockOne content
    section_options = []
    for block in content_blocks:
        if block.polymorphic_ctype.model == 'headingblockone':
            section_options.append((
                slugify(block.text),
                block.text
            ))
    
    # Add a default "Other" option if no headings found or for general edits
    if not section_options:
        section_options = [('other', 'Other')]
    else:
        section_options.append(('other', 'Other'))
    
    context = {
        'chapter': chapter,
        'app_label': app_label,
        'app_title': config['title'],
        'section_options': section_options,
    }
    
    return render(request, 'editor/suggest_edit.html', context)

@login_required
@reviewer_required
def district_intro_edit(request, district_id):
    """View for editing district introduction and quick facts"""
    district = get_object_or_404(District.objects.select_related('state'), id=district_id)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Update district introduction
                district.introduction = request.POST.get('introduction', '')
                district.save()
                
                # Handle quick facts
                # First, get existing quick facts
                existing_facts = list(district.quick_facts.all())
                
                # Get submitted quick facts data
                fact_ids = request.POST.getlist('fact_id[]')
                fact_titles = request.POST.getlist('fact_title[]')
                fact_contents = request.POST.getlist('fact_content[]')
                
                # Track which facts were submitted
                submitted_fact_ids = []
                
                # Update or create facts
                for i, (fact_id, title, content) in enumerate(zip(fact_ids, fact_titles, fact_contents)):
                    if title.strip():  # Only process if title is not empty
                        if fact_id and fact_id.isdigit():
                            # Update existing fact
                            fact_id = int(fact_id)
                            try:
                                fact = DistrictQuickFact.objects.get(id=fact_id, district=district)
                                fact.title = title
                                fact.content = content
                                fact.save()
                                submitted_fact_ids.append(fact_id)
                            except DistrictQuickFact.DoesNotExist:
                                pass
                        else:
                            # Create new fact
                            new_fact = DistrictQuickFact.objects.create(
                                district=district,
                                title=title,
                                content=content
                            )
                            submitted_fact_ids.append(new_fact.id)
                
                # Delete facts that weren't submitted
                facts_to_delete = district.quick_facts.exclude(id__in=submitted_fact_ids)
                facts_to_delete.delete()
                
            messages.success(request, 'District information updated successfully!')
            return redirect(district.get_absolute_url())
            
        except Exception as e:
            messages.error(request, f'Error updating district information: {str(e)}')
    
    # Get existing quick facts
    quick_facts = district.quick_facts.all()
    
    context = {
        'district': district,
        'quick_facts': quick_facts,
    }
    
    return render(request, 'editor/introedit.html', context)


def suggest_intro_view(request, district_id):
    """View for suggesting edits to district introduction"""
    district = get_object_or_404(
        District.objects.select_related('state'),
        id=district_id
    )
    
    if request.method == 'POST':
        # Create suggestion from form data
        suggestion = IntroductionEdit(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            user=request.user if request.user.is_authenticated else None,
            district=district,
            section=request.POST.get('section', 'introduction'),
            edit_type=request.POST.get('edit_type'),
            current_text=request.POST.get('current_text', ''),
            suggested_text=request.POST.get('suggested_text'),
            reason=request.POST.get('reason'),
            sources=request.POST.get('sources', ''),
            notify_on_review=request.POST.get('notification') == 'on',
        )
        
        # Handle file upload
        if request.FILES.get('file-upload'):
            suggestion.supporting_file = request.FILES['file-upload']
        
        suggestion.save()
        
        messages.success(request, 'Your edit suggestion has been submitted successfully!')
        return redirect('home:district_detail', state_slug=district.state.slug, district_slug=district.slug)
    
    context = {
        'district': district,
    }
    
    return render(request, 'editor/suggest_intro.html', context)