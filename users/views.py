from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
# Create your views here.


def user_login(request):
    if request.user.is_authenticated:
        next_url = request.GET.get('next')
        if next_url:
            return redirect(next_url)
        return redirect('user_profile')
    
    if request.method == "POST":
        email =request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, "Email and password are required.")
            return render(request, 'users/login.html')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request,user)

            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            
            messages.success(request, f"Login successful. {user.first_name or user.email}")
            return redirect('user_profile')
        else:
            messages.error(request, "Invalid email or password.")
    return render(request, 'users/login.html')



def custom_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect('users:login')
    else:
        messages.warning(request, "You are not logged in.")



def forgot_password(request):
    return render(request, 'users/forgot_password.html')


def register(request):
    return render(request,'users/register.html')
