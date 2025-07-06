

import logging
import zipfile
import io
import os
from bs4 import BeautifulSoup, Tag
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from django.utils.text import slugify
from urllib.parse import urlparse, parse_qs
from django.core.files.base import ContentFile

from .forms import DataImportForm
from culture.models import (
    CulturalChapter, ContentBlock, HeadingBlockOne, HeadingBlockTwo,
    HeadingBlockThree, ParagraphBlock, ImageBlock, ReferenceBlock
)

logger = logging.getLogger(__name__)

def _parse_and_save_blocks(html_content, chapter, image_data_map):
    """
    Parses HTML content, attaching images from the provided map and merging paragraphs.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    body = soup.find('body')

    if not body: raise ValueError("Invalid HTML file: No <body> tag found.")

    ContentBlock.objects.filter(chapter=chapter).delete()
    
    elements = body.find_all(recursive=False)
    consumed_elements, order, in_references_section = set(), 0, False
    paragraph_html_buffer = []

    def save_buffered_paragraphs():
        nonlocal order
        if paragraph_html_buffer:
            full_html_content = "\n".join(paragraph_html_buffer)
            ParagraphBlock.objects.create(chapter=chapter, order=order, content=full_html_content)
            order += 1
            paragraph_html_buffer.clear()
            logger.info("Saved one combined ParagraphBlock.")

    for element in elements:
        if element in consumed_elements or not isinstance(element, Tag): continue

        # Handle References Section as a breaker
        if not in_references_section and element.name == 'h1' and 'references' in element.get_text(strip=True).lower():
            save_buffered_paragraphs()
            # Save the References heading first
            HeadingBlockOne.objects.create(chapter=chapter, order=order, text=element.get_text(strip=True))
            order += 1
            in_references_section = True
            logger.info("----> Saved References heading and switched to References parsing mode.")
            continue
        
        if in_references_section:
            save_buffered_paragraphs()
            if element.name == 'ul':
                for li in element.find_all('li'):
                    # Get the full text and extract link
                    full_text = li.get_text(strip=True)
                    link_tag = li.find('a')
                    raw_link = link_tag.get('href') if link_tag else None
                    
                    # Extract only the reference text (excluding link text)
                    if link_tag:
                        link_text = link_tag.get_text(strip=True)
                        # Remove the link text from the full text to get just the reference text
                        ref_text = full_text.replace(link_text, '').strip()
                        # Clean up any extra spaces or punctuation
                        ref_text = ' '.join(ref_text.split())
                    else:
                        ref_text = full_text
                    
                    # Clean the link URL
                    clean_link = raw_link
                    if raw_link and 'google.com/url' in raw_link:
                        real_url = parse_qs(urlparse(raw_link).query).get('q', [None])[0]
                        if real_url: clean_link = real_url
                    
                    ReferenceBlock.objects.create(chapter=chapter, order=order, text=ref_text, link=clean_link)
                    order += 1
        else:
            tag_name = element.name
            img_tag = element.find('img')
            is_breaker_tag = (tag_name in ['h1', 'h2', 'h3'] or img_tag is not None)

            if is_breaker_tag:
                save_buffered_paragraphs()
                # --- THIS IS THE NEW, DETAILED IMAGE HANDLING LOGIC ---
                if img_tag:
                    caption_text, caption_tag = "Image (no caption)", element.find_next_sibling('h4')
                    if caption_tag:
                        caption_text = caption_tag.get_text(strip=True)
                        consumed_elements.add(caption_tag)
                    
                    # Create the instance but don't save to the DB yet.
                    image_block = ImageBlock(chapter=chapter, order=order, caption=caption_text, alt_text=caption_text)
                    
                    # Try to find and attach the image from the zip file.
                    img_src = img_tag.get('src')
                    if img_src and image_data_map.get(img_src):
                        image_bytes = image_data_map[img_src]
                        file_name = os.path.basename(img_src)
                        # Attach the in-memory file to the ImageField
                        image_block.image.save(file_name, ContentFile(image_bytes), save=False)
                        logger.info(f"Attached '{img_src}' to new ImageBlock.")
                    else:
                        logger.warning(f"Image '{img_src}' found in HTML but NOT in the zip file. Block created without an image.")
                    
                    # Save the complete instance (with or without the image file).
                    image_block.save()
                    order += 1
                else:
                    model_map = {'h1': HeadingBlockOne, 'h2': HeadingBlockTwo, 'h3': HeadingBlockThree}
                    model_map[tag_name].objects.create(chapter=chapter, order=order, text=element.get_text(strip=True))
                    order += 1
            elif tag_name in ['p', 'ul', 'ol', 'table']:
                text_content = element.get_text(strip=True)
                if text_content and not (text_content.startswith('<Insert') and text_content.endswith('>')):
                    content_html = str(element).strip()
                    paragraph_html_buffer.append(content_html)
    
    save_buffered_paragraphs()
    return order

@transaction.atomic
def import_data_view(request):
    if request.method == 'POST':
        form = DataImportForm(request.POST, request.FILES)
        if form.is_valid():
            chapter_name = form.cleaned_data['chapter_name']
            try:
                # --- PROCESS THE ZIP FILE (if provided) ---
                image_data_map = {}
                image_zip_file = form.cleaned_data.get('image_zip')
                if image_zip_file:
                    try:
                        # Unzip in memory to avoid writing to disk
                        with zipfile.ZipFile(image_zip_file, 'r') as zip_ref:
                            for file_name in zip_ref.namelist():
                                # Avoid mac-specific junk files and directories
                                if not file_name.startswith('__MACOSX') and not file_name.endswith('/'):
                                    image_data_map[file_name] = zip_ref.read(file_name)
                        messages.info(request, f"Processed {len(image_data_map)} images from the zip file.")
                    except zipfile.BadZipFile:
                        messages.error(request, "The provided image file was not a valid ZIP archive. No images were processed.")

                # Find or create the chapter
                chapter, _ = CulturalChapter.objects.get_or_create(district=form.cleaned_data['district'], name=chapter_name, defaults={'slug': slugify(chapter_name)})
                messages.warning(request, f"Found/created chapter '{chapter}'. Old content will be replaced.")
                
                # Call the parser, now with the image map
                html_content = form.cleaned_data['html_file'].read().decode('utf-8')
                blocks_count = _parse_and_save_blocks(html_content, chapter, image_data_map)
                
                messages.success(request, f"Successfully imported {blocks_count} content blocks.")
                return redirect(chapter.get_absolute_url())

            except Exception as e:
                logger.error(f"Import failed for chapter '{chapter_name}'. Error: {e}", exc_info=True)
                messages.error(request, f"A critical error occurred: '{e}'. The import was cancelled.")
                return redirect('importdata:import_data')
    else:
        form = DataImportForm()

    context = {'form': form, 'title': "Import Chapter Data and Images"}
    return render(request, 'importdata/import_form.html', context)