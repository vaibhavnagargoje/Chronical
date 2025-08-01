from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile, OTPVerification, PasswordResetToken

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fieldsets = (
        ('User Types', {
            'fields': ('is_super_admin', 'is_admin', 'is_reviewer', 'is_content_editor'),
            'description': 'Select user types (multiple selections allowed)'
        }),
        ('Status', {
            'fields': ('is_verified', 'is_active')
        }),
        ('Personal Information', {
            'fields': ('phone_number', 'date_of_birth', 'gender', 'bio', 'profile_picture', 'website')
        }),
        ('Address Information', {
            'fields': ('address', 'city', 'state', 'country', 'pin_code'),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        })
    )
    readonly_fields = ('created_at', 'updated_at')

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_user_types', 'get_is_verified')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'profile__is_admin', 'profile__is_reviewer', 'profile__is_content_editor', 'profile__is_super_admin', 'profile__is_verified')
    
    def get_user_types(self, obj):
        if hasattr(obj, 'profile'):
            return obj.profile.get_user_types()
        return 'No Profile'
    get_user_types.short_description = 'User Types'
    
    def get_is_verified(self, obj):
        if hasattr(obj, 'profile'):
            return obj.profile.is_verified
        return False
    get_is_verified.short_description = 'Verified'
    get_is_verified.boolean = True

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_user_types', 'phone_number', 'is_verified', 'is_active', 'created_at')
    list_filter = ('is_admin', 'is_reviewer', 'is_content_editor', 'is_super_admin', 'is_verified', 'is_active', 'gender', 'created_at')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'phone_number')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('User Types', {
            'fields': ('is_super_admin', 'is_admin', 'is_reviewer', 'is_content_editor'),
            'description': 'Select user types (multiple selections allowed)'
        }),
        ('Status', {
            'fields': ('is_verified', 'is_active')
        }),
        ('Personal Information', {
            'fields': ('phone_number', 'date_of_birth', 'gender', 'bio', 'profile_picture', 'website')
        }),
        ('Address Information', {
            'fields': ('address', 'city', 'state', 'country', 'pin_code'),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        })
    )

@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'otp', 'created_at', 'expires_at', 'is_expired')
    list_filter = ('created_at',)
    search_fields = ('email', 'username')
    readonly_fields = ('created_at', 'expires_at')

@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ('email', 'token', 'created_at', 'expires_at', 'used', 'is_valid')
    list_filter = ('used', 'created_at')
    search_fields = ('email',)
    readonly_fields = ('created_at', 'expires_at', 'token')

# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
readonly_fields = ('created_at', 'expires_at', 'token')

# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
