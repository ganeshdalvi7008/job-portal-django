from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from datetime import datetime, timedelta
from accounts.decorators import recruiter_required
from .models import Job
from .forms import JobForm
from profiles.models import RecruiterProfile, Company

def job_list_view(request):
    jobs = Job.objects.filter(status='approved').order_by('-created_at')
    
    # Search Query
    q = request.GET.get('q', '')
    if q:
        jobs = jobs.filter(
            Q(title__icontains=q) |
            Q(skills__icontains=q) |
            Q(location__icontains=q) |
            Q(company__company_name__icontains=q)
        )
        
    # Filters
    job_type = request.GET.get('job_type', '')
    if job_type:
        jobs = jobs.filter(job_type=job_type)
        
    work_mode = request.GET.get('work_mode', '')
    if work_mode:
        jobs = jobs.filter(work_mode=work_mode)
        
    location = request.GET.get('location', '')
    if location:
        jobs = jobs.filter(location__icontains=location)
        
    experience = request.GET.get('experience', '')
    if experience:
        jobs = jobs.filter(experience__icontains=experience)
        
    min_salary = request.GET.get('min_salary', '')
    if min_salary:
        try:
            jobs = jobs.filter(salary_max__gte=float(min_salary))
        except ValueError:
            pass

    date_posted = request.GET.get('date_posted', '')
    if date_posted:
        now = datetime.now()
        if date_posted == '24h':
            jobs = jobs.filter(created_at__gte=now - timedelta(days=1))
        elif date_posted == '3d':
            jobs = jobs.filter(created_at__gte=now - timedelta(days=3))
        elif date_posted == '7d':
            jobs = jobs.filter(created_at__gte=now - timedelta(days=7))

    # Pagination
    paginator = Paginator(jobs, 6) # 6 jobs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Unique locations and experiences for sidebar filters
    locations = Job.objects.filter(status='approved').values_list('location', flat=True).distinct()
    
    context = {
        'page_obj': page_obj,
        'q': q,
        'selected_job_type': job_type,
        'selected_work_mode': work_mode,
        'selected_location': location,
        'selected_experience': experience,
        'selected_min_salary': min_salary,
        'selected_date_posted': date_posted,
        'locations': locations,
        'total_jobs': jobs.count()
    }
    return render(request, 'jobs/list.html', context)


def job_detail_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    # Check if job is active/approved or if the current user is the owner/recruiter of this job
    if job.status != 'approved':
        if not request.user.is_authenticated or (request.user != job.recruiter and not request.user.is_superuser):
            raise PermissionDenied("This job posting is not active.")
            
    # Check if job seeker has already applied
    already_applied = False
    if request.user.is_authenticated and request.user.role == 'job_seeker':
        already_applied = job.applications.filter(job_seeker=request.user).exists()
        
    context = {
        'job': job,
        'already_applied': already_applied
    }
    return render(request, 'jobs/detail.html', context)


@login_required
@recruiter_required
def add_job_view(request):
    # Ensure recruiter has completed company profile
    try:
        profile = request.user.recruiter_profile
        if not profile.company:
            messages.warning(request, "Please create a Company Profile first before posting a job.")
            return redirect('manage_company')
    except RecruiterProfile.DoesNotExist:
        # Fallback to create profile
        RecruiterProfile.objects.create(user=request.user)
        messages.warning(request, "Please complete your profile details and company info first.")
        return redirect('edit_recruiter_profile')
        
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            job.company = profile.company
            job.save()
            messages.success(request, f"Job '{job.title}' posted successfully!")
            return redirect('manage_jobs')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = JobForm()
        
    return render(request, 'jobs/add.html', {'form': form})


@login_required
@recruiter_required
def edit_job_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    
    # Recruiter can only manage their own jobs
    if job.recruiter != request.user and not request.user.is_superuser:
        raise PermissionDenied("You are not authorized to edit this job posting.")
        
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, f"Job '{job.title}' updated successfully!")
            return redirect('manage_jobs')
        else:
            messages.error(request, "Failed to update the job. Please check details.")
    else:
        form = JobForm(instance=job)
        
    return render(request, 'jobs/edit.html', {'form': form, 'job': job})


@login_required
@recruiter_required
def delete_job_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    
    # Recruiter can only delete their own jobs
    if job.recruiter != request.user and not request.user.is_superuser:
        raise PermissionDenied("You are not authorized to delete this job posting.")
        
    if request.method == 'POST':
        job.delete()
        messages.success(request, "Job posting deleted successfully.")
        return redirect('manage_jobs')
        
    return render(request, 'jobs/delete_confirm.html', {'job': job})


@login_required
@recruiter_required
def manage_jobs_view(request):
    # Recruiter can view their posted jobs
    jobs = Job.objects.filter(recruiter=request.user).order_by('-created_at')
    return render(request, 'jobs/manage.html', {'jobs': jobs})
