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
from django.urls import reverse
from django.conf import settings
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
            return redirect('users:login_success')
        else:
            messages.error(request, "Invalid email or password.")
    return render(request, 'users/login.html')


def login_success(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to view this page.")
        return redirect('users:login')
    
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'users/login_success.html', context)


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
            password=password,  # Store the raw password temporarily
            first_name=first_name,
            last_name=last_name,
            otp=otp
        )

        try:
            send_mail(
                'The Districts Project - OTP Verification',
                f'Thank you for registering with the Districts Project.\n\nYour OTP is {otp}\n\nRegards,\nCentre for Knowledge Alternatives, FLAME University',
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


def verify_otp(request):
    email = request.session.get('otp_email')
    if not email:
        messages.error(request,"No pending Verification found. Please register again.")
        return redirect('users:register')

    if request.method == "POST":
        entered_otp = request.POST.get('otp')
        try:
            otp_record = OTPVerification.objects.get(email=email)
            if otp_record.is_expired():
                del request.session['otp_email']
                messages.error(request,"OTP has expired. Please request a new one.")
                return redirect('users:register')
            
            if otp_record.otp == entered_otp:
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=otp_record.password,  # Django will hash this password properly
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
            



def registration_success(request):
    return render(request, 'users/register_success.html')


def custom_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect('home:index')
    else:
        messages.warning(request, "You are not logged in.")



def forgot_password(request):
    if request.method=="POST":
        email = request.POST.get('email', '').strip()
        if not email:
            messages.error(request, "Email is required.")
            return render(request, 'users/forgot_password.html')
        
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email address.")
            return render(request, 'users/forgot_password.html')
        
        try:
            user = User.objects.get(email=email)
            PasswordResetToken.objects.filter(email=email, used=False).update(used=True)
            reset_token = PasswordResetToken.objects.create(email=email)
            
            reset_url = request.build_absolute_uri(
                reverse('users:reset_password', kwargs={'token': reset_token.token})
            )

            try:
                # Correct usage of Django's send_mail
                subject = 'Password Reset Request'
                message = f"""
                Hello {user.first_name or user.email},
                
                You requested a password reset. Please click the link below to reset your password:
                
                {reset_url}
                
                If you did not request this password reset, please ignore this email.
                """
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [email]
                
                success = send_mail(
                    subject=subject,
                    message=message,
                    from_email=from_email,
                    recipient_list=recipient_list,
                    fail_silently=False,
                )
                
                if success:
                    messages.success(request, "Password reset link has been sent to your registered email.")
                    return redirect('users:login')
                else:
                    messages.error(request, "Failed to send password reset link. Please try again later.")
                    return render(request, 'users/forgot_password.html')
            
            except Exception as e:
                messages.error(request, f"Failed to send password reset email. Please try again")
                return render(request, 'users/forgot_password.html')
        except User.DoesNotExist:
            messages.success(request, "If an account with this email exists, a password reset link will be sent to it." )

            return redirect('users:login')
        

    return render(request, 'users/forgot_password.html')


def reset_password(request, token):
    """Handle password reset with token."""
    try:
        reset_token = PasswordResetToken.objects.get(token=token)
        
        if not reset_token.is_valid():
            messages.error(request, "This password reset link has expired or is invalid. Please request a new one.")
            return redirect('users:forgot_password')
        
        try:
            user = User.objects.get(email=reset_token.email)
        except User.DoesNotExist:
            messages.error(request, "Invalid reset link.")
            return redirect('users:forgot_password')
        
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            # Validation
            if not all([new_password, confirm_password]):
                messages.error(request, "Both password fields are required")
                return render(request, 'users/reset_password.html', {'token': token})
            
            if new_password != confirm_password:
                messages.error(request, "Passwords don't match")
                return render(request, 'users/reset_password.html', {'token': token})
            
            if len(new_password) < 6:
                messages.error(request, "Password must be at least 6 characters long")
                return render(request, 'users/reset_password.html', {'token': token})
            
            # Update password
            user.set_password(new_password)
            user.save()
            
            # Mark token as used
            reset_token.used = True
            reset_token.save()
            
            messages.success(request, "Your password has been reset successfully! Please login with your new password.")
            return redirect('users:login')
        
        return render(request, 'users/reset_password.html', {
            'token': token,
            'user_email': user.email
        })
        
    except PasswordResetToken.DoesNotExist:
        messages.error(request, "Invalid password reset link.")
        return redirect('users:forgot_password')





def user_profile(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to view your profile.")
        return redirect('users:login')
    
    user = request.user
    profile = user.profile
    
    if request.method == 'POST':
        # Update User model fields
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.save()
        
        # Update Profile model fields
        profile.phone_number = request.POST.get('phone_number', '')
        profile.address = request.POST.get('address', '')
        profile.city = request.POST.get('city', '')
        profile.state = request.POST.get('state', '')
        profile.country = request.POST.get('country', '')
        profile.pin_code = request.POST.get('pin_code', '')
        profile.bio = request.POST.get('bio', '')
        profile.website = request.POST.get('website', '')
        profile.gender = request.POST.get('gender', '')
        
        # Handle date of birth
        dob = request.POST.get('date_of_birth')
        if dob:
            profile.date_of_birth = dob
        
        # Handle profile picture
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
        
        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('users:user_profile')
    
    context = {
        'user': user,
        'profile': profile,
    }
    return render(request, 'users/user_profile.html', context)


def change_password(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to change your password.")
        return redirect('users:login')
    
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validation
        if not all([current_password, new_password, confirm_password]):
            messages.error(request, "All password fields are required.")
            return render(request, 'users/change_password.html')
        
        # Check if current password is correct
        if not request.user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return render(request, 'users/change_password.html')
        
        # Check if new passwords match
        if new_password != confirm_password:
            messages.error(request, "New passwords don't match.")
            return render(request, 'users/change_password.html')
        
        # Check password length
        if len(new_password) < 8:
            messages.error(request, "New password must be at least 8 characters long.")
            return render(request, 'users/change_password.html')
        
        # Check if new password is different from current
        if current_password == new_password:
            messages.error(request, "New password must be different from current password.")
            return render(request, 'users/change_password.html')
        
        # Update password
        request.user.set_password(new_password)
        request.user.save()
        
        # Re-authenticate user to keep them logged in
        user = authenticate(request, username=request.user.email, password=new_password)
        if user:
            login(request, user)
        
        messages.success(request, "Password changed successfully!")
        return redirect('users:user_profile')
    
    return render(request, 'users/change_password.html')


