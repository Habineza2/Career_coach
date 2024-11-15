
from django.contrib import admin
from django.urls import path
from users.views import user_profile_form, UserProfileListCreate, user_profile_view
from django.views.generic import TemplateView
from users import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='users/home.html'), name='home'),
    path('user_profile_form/', user_profile_form, name='user_profile_form'), 
    path('profiles/<int:profile_id>/delete/', views.user_profile_delete, name='user_profile_delete'),
    path('profiles/<int:profile_id>/', views.user_profile_detail, name='user_profile_detail'),
    path('profiles/<int:profile_id>/edit/', user_profile_form, name='user_profile_edit'), 
    path('profiles/success/', TemplateView.as_view(template_name='users/success.html'), name='user_profile_success'),  # Success page
    path('profiles/create/', UserProfileListCreate.as_view(), name='user_profile_create'),  # Adjusted path for creating profiles
    path('profiles/', views.user_profile_list, name='user_profile_list'),  # View for listing profiles
    
    path('user_profile/view/', user_profile_view, name='user_profile_view'),
    path('login/', views.user_login, name='login'),  # Add this line
    path('logout/', views.user_logout, name='logout'),
    
    
    
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('notification/<int:notification_id>/read/', views.mark_notification_as_read, name='mark_notification_as_read'),
    
    
    
    path('post-job/', views.post_job, name='post_job'),
    path('jobs/', views.job_list, name='job_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
