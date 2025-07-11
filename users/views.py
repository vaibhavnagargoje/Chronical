from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import random
from .models import OTPVerification, PasswordResetToken
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
# Create your views here.


def user_login(request):
    if request.user.is_authenticated:
        next_url = request.GET.get('next')
        if next_url:
            return redirect(next_url)
        return redirect('users:user_profile')
    
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
            return redirect('users:user_profile')
        else:
            messages.error(request, "Invalid email or password.")
    return render(request, 'users/login.html')


def register(request):
    if request.method == "POST":
        email= request.POST.get('email')
        password= request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name','')
        last_name = request.POST.get('last_name','')

        if not all([email,password,confirm_password]):
            messages.error(request, "Email and Password fields are required.")
            return render(request, 'users/register.html')
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'users/register.html')
        
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return render(request, 'users/register.html')
        
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email address.")
            return render(request, 'users/register.html')
        
        if User.objects.filter(username=email).exists():
            messages.error(request, "An Account with this email already exists.")
            return render(request, 'users/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, 'users/register.html')

        otp = str(random.randint(1000, 9999))

        OTPVerification.objects.filter(email=email).delete()

        otp_record = OTPVerification.objects.create(
            email=email,
            username=email,
            password=make_password(password),
            first_name=first_name,
            last_name=last_name,
            otp=otp
        )

        try:
            send_mail(
                'OTP Verification for Registration',
                f'Your OTP is {otp}',
                'from@example.com',
                [email],
                fail_silently=False,
            )
            request.session['otp_email'] = email
            messages.success(request, "OTP sent to your email. Please enter it to complete registration.")
            return redirect('users:verify_otp')
        except Exception as e:
            print(f"Error sending OTP: {e}")
            messages.error(request, "Failed to send OTP. Please try again.")
            return render(request, 'users/register.html')

    return render(request,'users/register.html')


def verity_otp(request):
    email = request.session.get('otp_email')
    if not email:
        messages.error(request,"No pending Verification found. Please register again.")
        return redirect('users:register')

    if request.method == "POST":
        entered_otp = request.POST.get('otp')
        try:
            otp_record = OTPVerification.objects.get(email=email)
            if otp_record.is_expired():
                del (request)
                messages.error(request,"OTP has expired. Please request a new one.")
                return redirect('users:register')
            
            if otp_record.otp == entered_otp:
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=otp_record.password,
                    first_name=otp_record.first_name,
                    last_name=otp_record.last_name
                )

                otp_record.delete() 
                messages.success(request, "Registration successful. You can now log in.")
                return redirect('users:registration_success')
            else:
                messages.error(request,"Invalid OTP. Please try again.")
        except OTPVerification.DoesNotExist:
            messages.error(request,"No OTP record found. Please register again.")
            return redirect('users:register')
    return render(request, 'users/verify_otp.html', {'email': email})
            
                

def custom_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect('users:login')
    else:
        messages.warning(request, "You are not logged in.")



def forgot_password(request):
    return render(request, 'users/forgot_password.html')




def user_profile(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to view your profile.")
        return redirect('users:login')
    
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'users/user_profile.html', context)