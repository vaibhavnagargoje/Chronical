from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from home.models import State
from .models import CulturalChapter, CulturalSection, Heading, Subheading, Text, Image, Reference

def cultural_chapter_detail(request, state_slug, district_slug, chapter_slug):
    state = get_object_or_404(State, slug=state_slug)
    district = get_object_or_404(state.districts, slug=district_slug)
    chapter = get_object_or_404(district.cultural_chapters, slug=chapter_slug)
    
    # Get all sections in order
    sections = chapter.sections.all().order_by('order')
    
    combined_content = []
    
    # Process each section in order
    for section in sections:
        # Get all content for this section ordered by their individual order fields
        section_content = []
        
        # Add headings
        section_content.extend(
            {'type': 'heading', 'data': h} 
            for h in section.headings.all().order_by('order')
        )
        
        # Add subheadings
        section_content.extend(
            {'type': 'subheading', 'data': sh} 
            for sh in section.subheadings.all().order_by('order')
        )
        
        # Add texts
        section_content.extend(
            {'type': 'text', 'data': t} 
            for t in section.texts.all().order_by('order')
        )
        
        # Add images
        section_content.extend(
            {'type': 'image', 'data': i} 
            for i in section.images.all().order_by('order')
        )
        
        
        # Add references
        section_content.extend(
            {'type': 'reference', 'data': ref} 
            for ref in section.references.all().order_by('order')
        )
        
        # Sort section content by their individual order fields
        section_content.sort(key=lambda x: x['data'].order)
        
        combined_content.extend(section_content)

    context = {
        'state': state,
        'district': district,
        'chapter': chapter,
        'combined_content': combined_content,
    }
    return render(request, 'culture/chapter_detail.html', context)