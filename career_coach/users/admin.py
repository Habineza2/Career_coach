# users/admin.py

from django.contrib import admin
from .models import UserProfile, Job, JobApplication, Notification

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'experience_level', 'industry_preference')
    search_fields = ('name', 'email', 'career_goal', 'skills', 'industry_preference')
    list_filter = ('experience_level', 'industry_preference')
    ordering = ('name',)
    list_per_page = 20

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'salary', 'posted_date', 'is_active')
    search_fields = ('title', 'location')
    list_filter = ('is_active',)
    ordering = ('-posted_date',)
    list_per_page = 20

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at', 'is_read')
    search_fields = ('user__username', 'message')
    list_filter = ('is_read',)
    ordering = ('-created_at',)
    list_per_page = 20

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'submitted_at')
    search_fields = ('user__username', 'job__title')
    list_filter = ('submitted_at',)
    ordering = ('-submitted_at',)
    list_per_page = 20



admin.site.site_header = "Career Coach Admin"
admin.site.site_title = "Career Coach Administration"
admin.site.index_title = "Welcome to the Career Coach Admin Panel"