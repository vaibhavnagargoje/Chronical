from django.shortcuts import render

    
def people(request):
    return render(request, 'footersection/people.html')


def careers(request):
    return render(request, 'footersection/careers.html')


def disclaimer(request):
    return render(request, 'footersection/disclaimers.html')


def partnerships(request):
    return render(request, 'footersection/partnership.html')


def projects(request):
    return render(request, 'footersection/project.html')


def subscribe(request):
    return render(request, 'footersection/subscribe.html')


def terms(request):
    return render(request, 'footersection/terms-and-conditions.html')