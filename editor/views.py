# editor/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db import transaction
from django.contrib.auth.decorators import login_required
import json

from .forms import ChapterSelectForm
from home.models import District
from culture.models import (
    CulturalChapter, ContentBlock, HeadingBlockOne, HeadingBlockTwo,
    HeadingBlockThree, ParagraphBlock, ImageBlock, ReferenceBlock
)

# A dictionary to map string names to the actual model classes
BLOCK_TYPE_MAP = {
    'heading1': HeadingBlockOne,
    'heading2': HeadingBlockTwo,
    'heading3': HeadingBlockThree,
    'paragraph': ParagraphBlock,
    'image': ImageBlock,
    'reference': ReferenceBlock,
}

@login_required
def select_chapter_view(request):
    """
    View for the user to select which district and chapter to edit.
    On POST, it finds or creates the chapter and redirects to the editor.
    """
    if request.method == 'POST':
        form = ChapterSelectForm(request.POST)
        if form.is_valid():
            district = form.cleaned_data['district']
            chapter_name = form.cleaned_data['chapter_name']
            
            # Get the chapter object, or create it if it doesn't exist
            chapter, created = CulturalChapter.objects.get_or_create(
                district=district,
                name=chapter_name
            )
            return redirect(reverse('editor:chapter_editor', kwargs={'chapter_id': chapter.id}))
    else:
        form = ChapterSelectForm()

    context = {
        'form': form,
    }
    return render(request, 'editor/select_chapter.html', context)


@login_required
def chapter_editor_view(request, chapter_id):
    """
    The main editor view.
    Handles creating, updating, reordering, and deleting content blocks intelligently.
    """
    chapter = get_object_or_404(
        CulturalChapter.objects.select_related('district__state'),
        id=chapter_id
    )

    if request.method == 'POST':
        content_data_json = request.POST.get('content_data')
        if not content_data_json:
            return redirect(reverse('editor:chapter_editor', kwargs={'chapter_id': chapter.id}))

        content_data = json.loads(content_data_json)
        
        try:
            with transaction.atomic():
                # Get a set of all current block IDs for this chapter to track deletions.
                existing_block_ids = set(chapter.content_blocks.values_list('id', flat=True))
                submitted_block_ids = set()

                # Loop through submitted data to UPDATE existing or CREATE new blocks
                for order_index, block_data in enumerate(content_data):
                    block_id = block_data.pop('id', None)
                    block_type_str = block_data.get('type')

                    # --- UPDATE an existing block ---
                    if block_id:
                        submitted_block_ids.add(block_id)
                        try:
                            block_instance = ContentBlock.objects.get(id=block_id, chapter=chapter)
                            block_instance.order = order_index

                            if isinstance(block_instance, (HeadingBlockOne, HeadingBlockTwo, HeadingBlockThree)):
                                block_instance.text = block_data.get('text', '')
                            elif isinstance(block_instance, ParagraphBlock):
                                block_instance.content = block_data.get('content', '')
                            elif isinstance(block_instance, ReferenceBlock):
                                block_instance.text = block_data.get('text', '')
                                block_instance.link = block_data.get('link', '')
                            elif isinstance(block_instance, ImageBlock):
                                block_instance.caption = block_data.get('caption', '')
                                block_instance.alt_text = block_data.get('alt_text', '')
                                
                                image_file_id = block_data.get('image_id')
                                if image_file_id and request.FILES.get(image_file_id):
                                    block_instance.image = request.FILES[image_file_id]
                            
                            block_instance.save()
                        except ContentBlock.DoesNotExist:
                            continue 
                    
                    # --- CREATE a new block ---
                    else:
                        BlockModelClass = BLOCK_TYPE_MAP.get(block_type_str)
                        if not BlockModelClass:
                            continue
                        
                        block_data.pop('type', None) # We've already used it
                        block_data['chapter'] = chapter
                        block_data['order'] = order_index
                        
                        if block_type_str == 'image':
                             image_file_id = block_data.pop('image_id', None)
                             if image_file_id and request.FILES.get(image_file_id):
                                 block_data['image'] = request.FILES[image_file_id]
                             else:
                                 continue # Don't create an image block without an image file

                        BlockModelClass.objects.create(**block_data)

                # --- DELETE blocks that were removed on the frontend ---
                ids_to_delete = existing_block_ids - submitted_block_ids
                if ids_to_delete:
                    for block_id in ids_to_delete:
                        # Use try-except in case of a bad ID
                        try:
                           ContentBlock.objects.get(id=block_id).delete()
                        except ContentBlock.DoesNotExist:
                            continue

            return redirect(chapter.get_absolute_url())

        except Exception as e:
            # You should add more robust logging here in a real application
            print(f"Error saving content: {e}") 
            # Optionally add a message to the user
            # messages.error(request, f"An error occurred: {e}")
            return redirect(reverse('editor:chapter_editor', kwargs={'chapter_id': chapter.id}))

    # GET request logic
    content_blocks = chapter.content_blocks.all().get_real_instances()
    context = {'chapter': chapter, 'content_blocks': content_blocks}
    return render(request, 'editor/chapter_editor.html', context)