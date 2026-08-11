from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import FileResponse, Http404
from datetime import date
import os
from accounts.decorators import seeker_required, recruiter_required
from jobs.models import Job
from .models import Application
from .forms import ApplicationForm
from profiles.models import JobSeekerProfile

@login_required
@seeker_required
def apply_job_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    
    # 1. Job active check
    if job.status != 'approved':
        messages.error(request, "This job posting is not active.")
        return redirect('job_list')
        
    # 2. Deadline check
    if job.deadline < date.today():
        messages.error(request, "The application deadline for this job has passed.")
        return redirect('job_detail', job_id=job.id)
        
    # 3. Duplicate application check
    if Application.objects.filter(job=job, job_seeker=request.user).exists():
        messages.warning(request, "You have already applied for this job.")
        return redirect('job_detail', job_id=job.id)
        
    # Attempt to pre-populate resume from seeker profile
    seeker_profile, created = JobSeekerProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.job = job
            app.job_seeker = request.user
            # If no new file uploaded, check if profile has one
            if not request.FILES.get('resume') and seeker_profile.resume:
                app.resume = seeker_profile.resume
            elif not request.FILES.get('resume') and not seeker_profile.resume:
                form.add_error('resume', 'Please upload a resume to complete your application.')
                return render(request, 'applications/apply.html', {'form': form, 'job': job})
                
            app.save()
            messages.success(request, f"Successfully applied for {job.title}!")
            return redirect('my_applications')
    else:
        # Prepopulate with profile resume if available
        initial = {}
        if seeker_profile.resume:
            initial['resume'] = seeker_profile.resume
        form = ApplicationForm(initial=initial)
        
    return render(request, 'applications/apply.html', {
        'form': form, 
        'job': job, 
        'profile_resume': seeker_profile.resume
    })


@login_required
@seeker_required
def my_applications_view(request):
    apps = Application.objects.filter(job_seeker=request.user).order_by('-applied_at')
    return render(request, 'applications/my_applications.html', {'apps': apps})


@login_required
def application_detail_view(request, app_id):
    app = get_object_or_404(Application, id=app_id)
    
    # Permission Checks:
    # 1. Job seeker: can only see their own application
    # 2. Recruiter: can only see applications to their own jobs
    # 3. Admin: full access
    user = request.user
    if user.is_superuser or user.role == 'admin':
        pass
    elif user.role == 'job_seeker' and app.job_seeker == user:
        pass
    elif user.role == 'recruiter' and app.job.recruiter == user:
        pass
    else:
        raise PermissionDenied("You are not authorized to view this application.")
        
    return render(request, 'applications/detail.html', {'app': app})


@login_required
@recruiter_required
def update_application_status_view(request, app_id):
    app = get_object_or_404(Application, id=app_id)
    
    # Recruiter can only update status for applications on their own jobs
    if app.job.recruiter != request.user and not request.user.is_superuser:
        raise PermissionDenied("You are not authorized to manage this application.")
        
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Application.STATUS_CHOICES):
            app.status = new_status
            app.save()
            messages.success(request, f"Application status updated to '{app.get_status_display()}'")
        else:
            messages.error(request, "Invalid application status selected.")
            
    return redirect('application_detail', app_id=app.id)


@login_required
@recruiter_required
def job_applicants_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    
    # Verify ownership
    if job.recruiter != request.user and not request.user.is_superuser:
        raise PermissionDenied("You are not authorized to view applicants for this job.")
        
    apps = job.applications.all().order_by('-applied_at')
    return render(request, 'applications/applicants.html', {'job': job, 'apps': apps})


@login_required
def download_resume_view(request, app_id):
    app = get_object_or_404(Application, id=app_id)
    user = request.user
    
    # Permissions: seeker owner, recruiter of the job, or admin
    if user.is_superuser or user.role == 'admin':
        pass
    elif user.role == 'job_seeker' and app.job_seeker == user:
        pass
    elif user.role == 'recruiter' and app.job.recruiter == user:
        pass
    else:
        raise PermissionDenied("You are not authorized to download this resume.")
        
    if not app.resume:
        raise Http404("Resume not found.")
        
    file_path = app.resume.path
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
        filename = os.path.basename(file_path)
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    else:
        raise Http404("Resume file does not exist on server disk.")
