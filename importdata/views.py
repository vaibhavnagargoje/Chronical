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
import re

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

def _truncate_heading_text(text, max_length=250):
    """
    Truncate heading text to fit database constraints.
    Leaves a small buffer from the 255 character limit.
    """
    if not text:
        return ""
    
    text = text.strip()
    if len(text) <= max_length:
        return text
    
    # Truncate at word boundary
    truncated = text[:max_length]
    last_space = truncated.rfind(' ')
    if last_space > 0:
        truncated = truncated[:last_space]
    
    return truncated + "..."

def _truncate_text(text, max_length=3000):
    """
    Truncate text to a maximum length while preserving word boundaries.
    """
    if not text:
        return ""
    
    text = text.strip()
    if len(text) <= max_length:
        return text
    
    # Truncate at word boundary
    truncated = text[:max_length]
    last_space = truncated.rfind(' ')
    if last_space > 0:
        truncated = truncated[:last_space]
    
    return truncated + "..."

def _is_footnote_reference(element):
    """
    Check if an element is a footnote reference (like [1], [2], etc.)
    Returns True if it's a footnote, False otherwise.
    """
    text = element.get_text(strip=True)
    
    # Check if the text starts with a footnote pattern like [1], [2], etc.
    if re.match(r'^\[\d+\]', text):
        return True
    
    # Check if the element contains footnote-related links
    link_tag = element.find('a')
    if link_tag:
        href = link_tag.get('href', '')
        link_id = link_tag.get('id', '')
        
        # Check for footnote reference patterns in href or id
        if (href.startswith('#ftnt_ref') or href.startswith('#ftnt') or 
            link_id.startswith('ftnt') or 'ftnt_ref' in href):
            return True
    
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

    def process_reference_list(list_element):
        """
        Process both <ul> (bullet points) and <ol> (numbered lists) for references.
        """
        nonlocal order
        
        list_type = "bullet" if list_element.name == 'ul' else "numbered"
        logger.info(f"Processing {list_type} list for references")
        
        for li in list_element.find_all('li'):
            # Skip if this is a footnote reference
            if _is_footnote_reference(li):
                logger.info(f"Skipping footnote reference: {li.get_text(strip=True)[:30]}...")
                continue
            
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
            
            # Truncate reference text if needed
            ref_text = _truncate_text(ref_text, 2000)
            
            try:
                Reference.objects.create(chapter=chapter, order=order, text=ref_text, link=clean_link)
                order += 1
                logger.info(f"Saved Reference block from {list_type} list: '{ref_text[:30]}...' with link: {clean_link}")
            except Exception as e:
                logger.error(f"Error saving reference from {list_type} list: {e}")
                logger.error(f"Reference text length: {len(ref_text)}")

    def process_reference_paragraph(paragraph_element):
        """
        Process paragraph elements in references section to extract individual references.
        Handles complex paragraph structures with spans and links.
        """
        nonlocal order
        
        # Skip if this is a footnote reference
        if _is_footnote_reference(paragraph_element):
            logger.info(f"Skipping footnote reference: {paragraph_element.get_text(strip=True)[:30]}...")
            return
        
        # Get the full text content of the paragraph
        full_text = paragraph_element.get_text(strip=True)
        
        if not full_text:
            return
        
        # Find the first link in the paragraph
        link_tag = paragraph_element.find('a')
        
        if link_tag:
            # Extract the raw link
            raw_link = link_tag.get('href')
            link_text = link_tag.get_text(strip=True)
            
            # Clean the link URL (handle Google redirects)
            clean_link = raw_link
            if raw_link and 'google.com/url' in raw_link:
                real_url = parse_qs(urlparse(raw_link).query).get('q', [None])[0]
                if real_url: 
                    clean_link = real_url
                    logger.info(f"Cleaned Google redirect link: {raw_link} -> {clean_link}")
            
            # For the reference text, use the full paragraph text
            # This preserves the complete citation including author, title, etc.
            ref_text = full_text.strip()
            
            # Clean up any extra spaces
            ref_text = ' '.join(ref_text.split())
            
            # Truncate reference text if needed
            ref_text = _truncate_text(ref_text, 2000)
            
            try:
                # Create the reference block
                Reference.objects.create(chapter=chapter, order=order, text=ref_text, link=clean_link)
                order += 1
                logger.info(f"Saved Reference block from paragraph: '{ref_text[:50]}...' with link: {clean_link}")
            except Exception as e:
                logger.error(f"Error saving reference from paragraph: {e}")
                logger.error(f"Reference text length: {len(ref_text)}")
            
        else:
            # No links found, treat the entire paragraph as a reference without link
            ref_text = full_text.strip()
            ref_text = ' '.join(ref_text.split())
            
            # Truncate reference text if needed
            ref_text = _truncate_text(ref_text, 2000)
            
            try:
                Reference.objects.create(chapter=chapter, order=order, text=ref_text, link=None)
                order += 1
                logger.info(f"Saved Reference block from paragraph (no link): '{ref_text[:50]}...'")
            except Exception as e:
                logger.error(f"Error saving reference from paragraph (no link): {e}")
                logger.error(f"Reference text length: {len(ref_text)}")

    def process_reference_div(div_element):
        """
        Process div elements in references section, specifically handling nested paragraphs.
        """
        nonlocal order
        
        # Look for paragraph elements within the div
        paragraphs = div_element.find_all('p')
        
        if paragraphs:
            # Process each paragraph in the div
            for p in paragraphs:
                process_reference_paragraph(p)
        else:
            # If no paragraphs, treat the div itself as a reference
            if not _is_footnote_reference(div_element):
                process_reference_paragraph(div_element)

    for element in elements:
        if element in consumed_elements or not isinstance(element, Tag): 
            continue

        # Handle References Section as a breaker
        if not in_references_section and element.name == 'h1' and 'references' in element.get_text(strip=True).lower():
            save_buffered_paragraphs()
            # Save the References heading first (with text truncation)
            heading_text = _truncate_heading_text(element.get_text(strip=True))
            HeadingOne.objects.create(chapter=chapter, order=order, text=heading_text)
            order += 1
            in_references_section = True
            logger.info("----> Saved References heading and switched to References parsing mode.")
            continue
        
        if in_references_section:
            save_buffered_paragraphs()
            # Handle lists (bullet points and numbered lists)
            if element.name in ['ul', 'ol']:
                process_reference_list(element)
            # Handle div elements that might contain references
            elif element.name == 'div':
                process_reference_div(element)
            # Handle paragraph elements in references section
            elif element.name == 'p':
                process_reference_paragraph(element)
            # Handle other elements that might contain references
            elif element.name in ['span'] and element.get_text(strip=True):
                # Treat other elements with text as reference paragraphs
                if not _is_footnote_reference(element):
                    process_reference_paragraph(element)
            # Skip empty elements or elements with no meaningful content
            elif element.get_text(strip=True):
                # Fallback: treat any other element with text as a reference
                if not _is_footnote_reference(element):
                    process_reference_paragraph(element)
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
                    # Truncate heading text to fit database constraints
                    heading_text = _truncate_heading_text(element.get_text(strip=True))
                    model_map = {'h1': HeadingOne, 'h2': HeadingTwo, 'h3': HeadingThree}
                    
                    try:
                        model_map[tag_name].objects.create(chapter=chapter, order=order, text=heading_text)
                        order += 1
                        logger.info(f"Saved {tag_name} heading: '{heading_text[:50]}...'")
                    except Exception as e:
                        logger.error(f"Error saving {tag_name} heading: {e}")
                        logger.error(f"Heading text length: {len(heading_text)}")
                        logger.error(f"Heading text: {heading_text[:100]}...")
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