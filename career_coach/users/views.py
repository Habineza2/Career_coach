from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import generics
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from .models import UserProfile
from .serializers import UserProfileSerializer
from django.core.exceptions import ValidationError
from django.core.validators import validate_email




def user_profile_form(request):
    if request.method == 'POST':
        # Get data from the form
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        career_goal = request.POST.get('career_goal', '')
        skills = request.POST.get('skills', '')
        experience_level = request.POST.get('experience_level', '')
        industry_preference = request.POST.get('industry_preference', '')
        profile_picture = request.FILES.get('profile_picture')
        password = request.POST.get('password', '')

        # Validate email
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Invalid email format.')
            return render(request, 'users/user_profile_form.html')

        # Check if email already exists
        if UserProfile.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists. Please use a different email.')
            return render(request, 'users/user_profile_form.html')

        # Hash the password
        hashed_password = make_password(password)

        # Create and save the user profile
        user_profile = UserProfile(
            name=name,
            email=email,
            career_goal=career_goal,
            skills=skills,
            experience_level=experience_level,
            industry_preference=industry_preference,
            profile_picture=profile_picture,
            password=hashed_password
        )
        user_profile.save()
        messages.success(request, 'Profile created successfully!')
        return redirect('user_profile_success')

    return render(request, 'users/user_profile_form.html')



class UserProfileListCreate(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


def user_profile_list(request):
    profiles = UserProfile.objects.all()
    return render(request, 'users/user_profile_list.html', {'profiles': profiles})


def user_profile_delete(request, profile_id):
    profile = get_object_or_404(UserProfile, id=profile_id)
    profile.delete()
    messages.success(request, 'Profile deleted successfully!')
    return redirect('user_profile_list')


def user_profile_detail(request, profile_id):
    profile = get_object_or_404(UserProfile, id=profile_id)
    return render(request, 'users/user_profile_detail.html', {'profile': profile})


@login_required
def user_profile_view(request):
    user_profile = get_object_or_404(UserProfile, email=request.user.email)
    return render(request, 'users/user_profile_detail.html', {'profile': user_profile})




from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import UserProfile

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            # Retrieve the user profile using the email
            user_profile = UserProfile.objects.get(email=email)
            
            # Check the password against the hashed password
            if check_password(password, user_profile.password):
                # If the password is correct, store user information in the session
                request.session['user_id'] = user_profile.id  # Store the user ID in the session
                messages.success(request, 'You have logged in successfully!')
                return redirect('dashboard')  # Redirect to the success page
            else:
                messages.error(request, 'Invalid email or password.')  # Incorrect password
        except UserProfile.DoesNotExist:
            messages.error(request, 'Invalid email or password.')  # User does not exist

    return render(request, 'users/login.html')






@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have logged out successfully!')
    return redirect('home')




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job, Notification, UserProfile

@login_required
def dashboard(request):
    # Check if the UserProfile exists for the current user
    user_profile, created = UserProfile.objects.get_or_create(email=request.user.email, defaults={
        'name': request.user.username,
        'career_goal': '',  # Set any defaults as needed
        'skills': '',
        'experience_level': '',
        'industry_preference': '',
        'profile_picture': None,
        'password': request.user.password
    })

    # Get active jobs
    jobs = Job.objects.filter(is_active=True)

    # Get user notifications
    notifications = Notification.objects.filter(user=request.user, is_read=False)

    context = {
        'user_profile': user_profile,
        'jobs': jobs,
        'notifications': notifications
    }
    return render(request, 'users/dashboard.html', context)






from .models import Job

@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'users/job_detail.html', {'job': job})




from .models import Notification

@login_required
def mark_notification_as_read(request, notification_id):
    # Fetch notification associated with the logged-in user and mark as read
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('dashboard')







# views.py

from django.shortcuts import render, redirect
from .forms import JobForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required  # Ensures only admin can access this view
@login_required
def post_job(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()  # Save the job to the database
            return redirect('job_list')  # Redirect to the job list or success page
    else:
        form = JobForm()

    return render(request, 'post_job.html', {'form': form})



def job_list(request):
    jobs = Job.objects.filter(is_active=True)
    return render(request, 'job_list.html', {'jobs': jobs})

