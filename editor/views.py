# # editor/views.py

# from django.shortcuts import render, redirect, get_object_or_404
# from django.urls import reverse
# from django.db import transaction
# from django.contrib.auth.decorators import login_required
# import json

# from .forms import ChapterSelectForm
# from home.models import District
# from culture.models import (
#     CulturalChapter, ContentBlock, HeadingBlockOne, HeadingBlockTwo,
#     HeadingBlockThree, ParagraphBlock, ImageBlock, ReferenceBlock
# )

# # A dictionary to map string names to the actual model classes
# BLOCK_TYPE_MAP = {
#     'heading1': HeadingBlockOne,
#     'heading2': HeadingBlockTwo,
#     'heading3': HeadingBlockThree,
#     'paragraph': ParagraphBlock,
#     'image': ImageBlock,
#     'reference': ReferenceBlock,
# }

# @login_required
# def select_chapter_view(request):
#     """
#     View for the user to select which district and chapter to edit.
#     On POST, it finds or creates the chapter and redirects to the editor.
#     """
#     if request.method == 'POST':
#         form = ChapterSelectForm(request.POST)
#         if form.is_valid():
#             district = form.cleaned_data['district']
#             chapter_name = form.cleaned_data['chapter_name']
            
#             # Get the chapter object, or create it if it doesn't exist
#             chapter, created = CulturalChapter.objects.get_or_create(
#                 district=district,
#                 name=chapter_name
#             )
#             return redirect(reverse('editor:chapter_editor', kwargs={'chapter_id': chapter.id}))
#     else:
#         form = ChapterSelectForm()

#     context = {
#         'form': form,
#     }
#     return render(request, 'editor/select_chapter.html', context)


# @login_required
# def chapter_editor_view(request, chapter_id):
#     """
#     The main editor view.
#     Handles creating, updating, reordering, and deleting content blocks intelligently.
#     """
#     chapter = get_object_or_404(
#         CulturalChapter.objects.select_related('district__state'),
#         id=chapter_id
#     )

#     if request.method == 'POST':
#         content_data_json = request.POST.get('content_data')
#         if not content_data_json:
#             return redirect(reverse('editor:chapter_editor', kwargs={'chapter_id': chapter.id}))

#         content_data = json.loads(content_data_json)
        
#         try:
#             with transaction.atomic():
#                 # Get a set of all current block IDs for this chapter to track deletions.
#                 existing_block_ids = set(chapter.content_blocks.values_list('id', flat=True))
#                 submitted_block_ids = set()

#                 # Loop through submitted data to UPDATE existing or CREATE new blocks
#                 for order_index, block_data in enumerate(content_data):
#                     block_id = block_data.pop('id', None)
#                     block_type_str = block_data.get('type')

#                     # --- UPDATE an existing block ---
#                     if block_id:
#                         submitted_block_ids.add(block_id)
#                         try:
#                             block_instance = ContentBlock.objects.get(id=block_id, chapter=chapter)
#                             block_instance.order = order_index

#                             if isinstance(block_instance, (HeadingBlockOne, HeadingBlockTwo, HeadingBlockThree)):
#                                 block_instance.text = block_data.get('text', '')
#                             elif isinstance(block_instance, ParagraphBlock):
#                                 block_instance.content = block_data.get('content', '')
#                             elif isinstance(block_instance, ReferenceBlock):
#                                 block_instance.text = block_data.get('text', '')
#                                 block_instance.link = block_data.get('link', '')
#                             elif isinstance(block_instance, ImageBlock):
#                                 block_instance.caption = block_data.get('caption', '')
#                                 block_instance.alt_text = block_data.get('alt_text', '')
                                
#                                 image_file_id = block_data.get('image_id')
#                                 if image_file_id and request.FILES.get(image_file_id):
#                                     block_instance.image = request.FILES[image_file_id]
                            
#                             block_instance.save()
#                         except ContentBlock.DoesNotExist:
#                             continue 
                    
#                     # --- CREATE a new block ---
#                     else:
#                         BlockModelClass = BLOCK_TYPE_MAP.get(block_type_str)
#                         if not BlockModelClass:
#                             continue
                        
#                         block_data.pop('type', None) # We've already used it
#                         block_data['chapter'] = chapter
#                         block_data['order'] = order_index
                        
#                         if block_type_str == 'image':
#                              image_file_id = block_data.pop('image_id', None)
#                              if image_file_id and request.FILES.get(image_file_id):
#                                  block_data['image'] = request.FILES[image_file_id]
#                              else:
#                                  continue # Don't create an image block without an image file

#                         BlockModelClass.objects.create(**block_data)

#                 # --- DELETE blocks that were removed on the frontend ---
#                 ids_to_delete = existing_block_ids - submitted_block_ids
#                 if ids_to_delete:
#                     for block_id in ids_to_delete:
#                         # Use try-except in case of a bad ID
#                         try:
#                            ContentBlock.objects.get(id=block_id).delete()
#                         except ContentBlock.DoesNotExist:
#                             continue

#             return redirect(chapter.get_absolute_url())

#         except Exception as e:
#             # You should add more robust logging here in a real application
#             print(f"Error saving content: {e}") 
#             # Optionally add a message to the user
#             # messages.error(request, f"An error occurred: {e}")
#             return redirect(reverse('editor:chapter_editor', kwargs={'chapter_id': chapter.id}))

#     # GET request logic
#     content_blocks = chapter.content_blocks.all().get_real_instances()
#     context = {'chapter': chapter, 'content_blocks': content_blocks}
#     return render(request, 'editor/chapter_editor.html', context)








# editor/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db import transaction
from django.http import Http404
from django.contrib.auth.decorators import login_required
import json
from django.conf import settings
from .forms import ChapterSelectForm

# Import models from BOTH apps
from culture.models import (
    CulturalChapter, ContentBlock as CulturalContentBlock, HeadingBlockOne as CulturalH1,
    HeadingBlockTwo as CulturalH2, HeadingBlockThree as CulturalH3,
    ParagraphBlock as CulturalP, ImageBlock as CulturalImg, ReferenceBlock as CulturalRef
)
from statistic.models import (
    StatisticalChapter, StatisticContentBlock, HeadingBlockOne as StatH1,
    HeadingBlockTwo as StatH2, HeadingBlockThree as StatH3,
    ParagraphBlock as StatP, ImageBlock as StatImg, ReferenceBlock as StatRef,
    ChartBlock # Import the new block
)

# A central configuration to make views generic without rewriting the logic.
APP_CONFIG = {
    'culture': {
        'title': 'Cultural',
        'ChapterModel': CulturalChapter,
        'BaseBlockModel': CulturalContentBlock,
        'BLOCK_TYPE_MAP': {
            'heading1': CulturalH1, 'heading2': CulturalH2, 'heading3': CulturalH3,
            'paragraph': CulturalP, 'image': CulturalImg, 'reference': CulturalRef,
        }
    },
    'statistic': {
        'title': 'Statistical',
        'ChapterModel': StatisticalChapter,
        'BaseBlockModel': StatisticContentBlock,
        'BLOCK_TYPE_MAP': {
            'heading1': StatH1, 'heading2': StatH2, 'heading3': StatH3,
            'paragraph': StatP, 'image': StatImg, 'reference': StatRef,
            'chart': ChartBlock, # The new ChartBlock is mapped here
        }
    }
}

def get_app_config(app_label):
    """Helper function to get the config or raise a 404 error."""
    config = APP_CONFIG.get(app_label)
    if not config:
        raise Http404(f"Editor not configured for app: '{app_label}'")
    return config

@login_required
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

    if request.method == 'POST':
        content_data_json = request.POST.get('content_data')
        if not content_data_json:
            return redirect(reverse('editor:chapter_editor', kwargs={'app_label': app_label, 'chapter_id': chapter.id}))

        content_data = json.loads(content_data_json)
        
        try:
            with transaction.atomic():
                existing_block_ids = set(chapter.content_blocks.values_list('id', flat=True))
                submitted_block_ids = set()

                for order_index, block_data in enumerate(content_data):
                    block_id = block_data.pop('id', None)
                    block_type_str = block_data.get('type')
                
                    if block_id:
                        submitted_block_ids.add(int(block_id))
                        try:
                            block_instance = BaseBlockModel.objects.get(id=block_id, chapter=chapter).get_real_instance()
                            block_instance.order = order_index
                            
                            # Your original logic is preserved perfectly here.
                            # We just added the `elif` for ChartBlock.
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
                                image_file_id = block_data.get('image_id')
                                if image_file_id and request.FILES.get(image_file_id):
                                    block_instance.image = request.FILES[image_file_id]
                            elif isinstance(block_instance, ChartBlock):
                                block_instance.title = block_data.get('title', '')
                                chart_file_id = block_data.get('chart_file_id')
                                if chart_file_id and request.FILES.get(chart_file_id):
                                    block_instance.chart_html_file = request.FILES[chart_file_id]

                            block_instance.save()
                        except BaseBlockModel.DoesNotExist:
                            continue 
                    
                    # --- CREATE a new block ---
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

                # --- DELETE blocks removed on the frontend ---
                ids_to_delete = existing_block_ids - submitted_block_ids
                if ids_to_delete:
                    # Your original loop structure, preserved
                    for block_id in ids_to_delete:
                        try:
                           BaseBlockModel.objects.get(id=block_id).delete()
                        except BaseBlockModel.DoesNotExist:
                            continue

            return redirect(chapter.get_absolute_url())

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
    }
     # Clean up TinyMCE instances before rendering
    if hasattr(settings, 'TINYMCE_JS_URL'):
        settings.TINYMCE_JS_URL = settings.STATIC_URL + 'tinymce/tinymce.min.js'
    return render(request, 'editor/chapter_editor.html', context)