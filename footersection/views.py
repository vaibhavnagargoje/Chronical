from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from django.contrib import messages
from .models import Project, Partnership, Careers, Terms, Disclaimer, Message



def super_admin_required(view_func):
    """Decorator to check if user has super admin permissions"""
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to login page
        
        # Check if user has reviewer or super admin permissions
        if not (hasattr(request.user, 'profile') and request.user.profile.is_super_admin):
            raise PermissionDenied("You don't have permission to access the editor.")
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view



def people(request):
    return render(request, 'footersection/people.html')


def careers(request):
    career = Careers.objects.first()
    if not career:
        career = Careers.objects.create()
    
    context = {
        'career': career
    }
    return render(request, 'footersection/suggest-edits.html', context)

@login_required
@super_admin_required
def edit_careers(request):
    career = Careers.objects.first()
    if not career:
        career = Careers.objects.create()
    
    if request.method == 'POST':
        text = request.POST.get('text', '')
        career.text = text
        career.save()
        messages.success(request, 'Careers content updated successfully!')
        return redirect('footersection:suggest_edits')
    
    context = {
        'career': career,
        'editing': True
    }
    return render(request, 'footersection/suggest-edits.html', context)


def disclaimer(request):
    disclaimer_obj = Disclaimer.objects.first()
    if not disclaimer_obj:
        disclaimer_obj = Disclaimer.objects.create()
    
    context = {
        'disclaimer': disclaimer_obj
    }
    return render(request, 'footersection/disclaimers.html', context)

@login_required
@super_admin_required
def edit_disclaimer(request):
    disclaimer_obj = Disclaimer.objects.first()
    if not disclaimer_obj:
        disclaimer_obj = Disclaimer.objects.create()
    
    if request.method == 'POST':
        text = request.POST.get('text', '')
        disclaimer_obj.text = text
        disclaimer_obj.save()
        messages.success(request, 'Disclaimer content updated successfully!')
        return redirect('footersection:disclaimers')
    
    context = {
        'disclaimer': disclaimer_obj,
        'editing': True
    }
    return render(request, 'footersection/disclaimers.html', context)


def partnerships(request):
    partnership = Partnership.objects.first()
    if not partnership:
        partnership = Partnership.objects.create()
    
    context = {
        'partnership': partnership
    }
    return render(request, 'footersection/partnership.html', context)

@login_required
@super_admin_required
def edit_partnership(request):
    partnership = Partnership.objects.first()
    if not partnership:
        partnership = Partnership.objects.create()
    
    if request.method == 'POST':
        text = request.POST.get('text', '')
        partnership.text = text
        partnership.save()
        messages.success(request, 'Partnership content updated successfully!')
        return redirect('footersection:partnership')
    
    context = {
        'partnership': partnership,
        'editing': True
    }
    return render(request, 'footersection/partnership.html', context)


def projects(request):
    project = Project.objects.first()  # Get the first project entry
    if not project:
        project = Project.objects.create()  # Create if doesn't exist
    
    context = {
        'project': project
    }
    return render(request, 'footersection/project.html', context)

@login_required
@super_admin_required
def edit_project(request):
    project = Project.objects.first()
    if not project:
        project = Project.objects.create()
    
    if request.method == 'POST':
        text = request.POST.get('text', '')
        project.text = text
        project.save()
        messages.success(request, 'Project content updated successfully!')
        return redirect('footersection:project')
    
    context = {
        'project': project,
        'editing': True
    }
    return render(request, 'footersection/project.html', context)


def subscribe(request):
    return render(request, 'footersection/subscribe.html')


def terms(request):
    terms_obj = Terms.objects.first()
    if not terms_obj:
        terms_obj = Terms.objects.create()
    
    context = {
        'terms': terms_obj
    }
    return render(request, 'footersection/terms-and-conditions.html', context)

@login_required
@super_admin_required
def edit_terms(request):
    terms_obj = Terms.objects.first()
    if not terms_obj:
        terms_obj = Terms.objects.create()
    
    if request.method == 'POST':
        text = request.POST.get('text', '')
        terms_obj.text = text
        terms_obj.save()
        messages.success(request, 'Terms content updated successfully!')
        return redirect('footersection:terms')
    
    context = {
        'terms': terms_obj,
        'editing': True
    }
    return render(request, 'footersection/terms-and-conditions.html', context)



def leave_us_a_message(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message_content = request.POST.get('message')
        
        # Create and save the message
        Message.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message_content
        )
        messages.success(request, 'Thank you for your message! We will get back to you soon.')
        return redirect('footersection:leave_us_a_message')
    return render(request, 'footersection/leave_us_a_message.html')