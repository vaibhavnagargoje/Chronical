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
from django.http import JsonResponse

from .forms import DataImportForm
from culture.models import (
    CulturalChapter, ContentBlock, HeadingBlockOne, HeadingBlockTwo,
    HeadingBlockThree, ParagraphBlock, ImageBlock, ReferenceBlock
)
# Import statistic models
from statistic.models import (
    StatisticalChapter, StatisticContentBlock, HeadingBlockOne as StatHeadingBlockOne,
    HeadingBlockTwo as StatHeadingBlockTwo, HeadingBlockThree as StatHeadingBlockThree,
    ParagraphBlock as StatParagraphBlock, ImageBlock as StatImageBlock,
    ReferenceBlock as StatReferenceBlock
)

logger = logging.getLogger(__name__)

def _clear_existing_blocks(chapter, app_type='culture'):
    """
    Safely clear all existing content blocks for a chapter.
    Handles polymorphic deletion properly.
    """
    try:
        if app_type == 'culture':
            # Get all content blocks for this chapter
            existing_blocks = ContentBlock.objects.filter(chapter=chapter)
            count = existing_blocks.count()
            
            # Delete each block individually to ensure proper polymorphic deletion
            for block in existing_blocks:
                block.delete()
            
            logger.info(f"Deleted {count} existing content blocks for culture chapter: {chapter.name}")
            
        else:  # statistic
            # Get all content blocks for this chapter
            existing_blocks = StatisticContentBlock.objects.filter(chapter=chapter)
            count = existing_blocks.count()
            
            # Delete each block individually to ensure proper polymorphic deletion
            for block in existing_blocks:
                block.delete()
            
            logger.info(f"Deleted {count} existing content blocks for statistic chapter: {chapter.name}")
            
        return True
        
    except Exception as e:
        logger.error(f"Error clearing existing blocks for chapter {chapter.name}: {e}")
        return False

def _parse_and_save_blocks(html_content, chapter, image_data_map, app_type='culture'):
    """
    Parses HTML content, attaching images from the provided map and merging paragraphs.
    Now handles both culture and statistic blocks.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    body = soup.find('body')

    if not body: 
        raise ValueError("Invalid HTML file: No <body> tag found.")

    # Choose the correct models based on app_type
    if app_type == 'culture':
        ContentBlockClass = ContentBlock
        HeadingOne = HeadingBlockOne
        HeadingTwo = HeadingBlockTwo
        HeadingThree = HeadingBlockThree
        Paragraph = ParagraphBlock
        Image = ImageBlock
        Reference = ReferenceBlock
    else:  # statistic
        ContentBlockClass = StatisticContentBlock
        HeadingOne = StatHeadingBlockOne
        HeadingTwo = StatHeadingBlockTwo
        HeadingThree = StatHeadingBlockThree
        Paragraph = StatParagraphBlock
        Image = StatImageBlock
        Reference = StatReferenceBlock
    
    elements = body.find_all(recursive=False)
    consumed_elements, order, in_references_section = set(), 0, False
    paragraph_html_buffer = []

    def save_buffered_paragraphs():
        nonlocal order
        if paragraph_html_buffer:
            full_html_content = "\n".join(paragraph_html_buffer)
            
            # Process any reference links in the paragraphs to make sure they work
            soup_para = BeautifulSoup(full_html_content, 'html.parser')
            
            # Find all links and process them
            for link in soup_para.find_all('a'):
                href = link.get('href', '')
                
                # Clean Google redirected links
                if href and 'google.com/url' in href:
                    real_url = parse_qs(urlparse(href).query).get('q', [None])[0]
                    if real_url: 
                        link['href'] = real_url
                        logger.info(f"Cleaned Google redirect link: {href} -> {real_url}")
            
            # Save the updated paragraph with cleaned links
            Paragraph.objects.create(chapter=chapter, order=order, content=str(soup_para))
            order += 1
            paragraph_html_buffer.clear()
            logger.info("Saved one combined ParagraphBlock.")

    for element in elements:
        if element in consumed_elements or not isinstance(element, Tag): 
            continue

        # Handle References Section as a breaker
        if not in_references_section and element.name == 'h1' and 'references' in element.get_text(strip=True).lower():
            save_buffered_paragraphs()
            # Save the References heading first
            HeadingOne.objects.create(chapter=chapter, order=order, text=element.get_text(strip=True))
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
                        if real_url: 
                            clean_link = real_url
                    
                    Reference.objects.create(chapter=chapter, order=order, text=ref_text, link=clean_link)
                    order += 1
                    logger.info(f"Saved Reference block: '{ref_text[:30]}...' with link: {clean_link}")
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
                    image_block = Image(chapter=chapter, order=order, caption=caption_text, alt_text=caption_text)
                    
                    # Try to find and attach the image from the zip file.
                    img_src = img_tag.get('src')
                    basename = os.path.basename(img_src) if img_src else ""
                    
                    # Try different ways to match the image
                    image_bytes = None
                    if img_src and img_src in image_data_map:
                        image_bytes = image_data_map[img_src]
                        logger.info(f"Found image using full path: '{img_src}'")
                    elif basename and basename in image_data_map:
                        image_bytes = image_data_map[basename]
                        logger.info(f"Found image using basename: '{basename}'")
                    
                    if image_bytes:
                        file_name = basename or "image.jpg"
                        # Attach the in-memory file to the ImageField
                        image_block.image.save(file_name, ContentFile(image_bytes), save=False)
                        logger.info(f"Attached image to new ImageBlock.")
                    else:
                        logger.warning(f"Image '{img_src}' found in HTML but NOT in the zip file. Block created without an image.")
                    
                    # Save the complete instance (with or without the image file).
                    image_block.save()
                    order += 1
                else:
                    model_map = {'h1': HeadingOne, 'h2': HeadingTwo, 'h3': HeadingThree}
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
            app_choice = form.cleaned_data['app_choice']
            
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
                                    image_data = zip_ref.read(file_name)
                                    # Store both by full path and basename for flexible lookup
                                    image_data_map[file_name] = image_data
                                    image_data_map[os.path.basename(file_name)] = image_data
                        
                        # Count unique images (not counting duplicates from basename storage)
                        unique_images = set(os.path.basename(name) for name in image_data_map.keys())
                        messages.info(request, f"Processed {len(unique_images)} images from the zip file.")
                    except zipfile.BadZipFile:
                        messages.error(request, "The provided image file was not a valid ZIP archive. No images were processed.")

                # Find or create the chapter based on app_choice
                if app_choice == 'culture':
                    chapter, created = CulturalChapter.objects.get_or_create(
                        district=form.cleaned_data['district'], 
                        name=chapter_name, 
                        defaults={'slug': slugify(chapter_name)}
                    )
                else:  # statistic
                    chapter, created = StatisticalChapter.objects.get_or_create(
                        district=form.cleaned_data['district'], 
                        name=chapter_name, 
                        defaults={'slug': slugify(chapter_name)}
                    )
                
                # Handle existing vs new chapter
                if created:
                    messages.info(request, f"Created new chapter '{chapter}'.")
                else:
                    messages.warning(request, f"Chapter '{chapter}' already exists. Replacing all content with new data.")
                    
                    # Clear existing blocks before adding new ones
                    if not _clear_existing_blocks(chapter, app_choice):
                        raise Exception("Failed to clear existing content blocks")
                
                # Process the HTML content
                html_content = form.cleaned_data['html_file'].read().decode('utf-8')
                
                # Pre-process HTML to improve reference parsing
                soup = BeautifulSoup(html_content, 'html.parser')
                
                # Fix links in the document to ensure they're clean
                for link in soup.find_all('a'):
                    href = link.get('href', '')
                    if href and 'google.com/url' in href:
                        real_url = parse_qs(urlparse(href).query).get('q', [None])[0]
                        if real_url:
                            link['href'] = real_url
                
                # Process the modified HTML content
                blocks_count = _parse_and_save_blocks(str(soup), chapter, image_data_map, app_choice)
                
                if created:
                    messages.success(request, f"Successfully created new chapter with {blocks_count} content blocks.")
                else:
                    messages.success(request, f"Successfully replaced chapter content with {blocks_count} new content blocks.")
                
                return redirect(chapter.get_absolute_url())

            except Exception as e:
                logger.error(f"Import failed for chapter '{chapter_name}'. Error: {e}", exc_info=True)
                messages.error(request, f"A critical error occurred: '{e}'. The import was cancelled.")
                return redirect('importdata:import_data')
    else:
        form = DataImportForm()

    context = {'form': form, 'title': "Import Chapter Data and Images"}
    return render(request, 'importdata/import_form.html', context)

def get_chapter_options(request):
    """API endpoint to get chapter options for both culture and statistic apps"""
    from culture.models import CulturalChapter
    from statistic.models import StatisticalChapter
    
    data = {
        'culture': list(CulturalChapter.CHAPTER_CHOICES),
        'statistic': list(StatisticalChapter.CHAPTER_CHOICES)
    }
    
    return JsonResponse(data)