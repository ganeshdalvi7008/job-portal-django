from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.decorators import seeker_required, recruiter_required, admin_required
from django.contrib.auth import get_user_model
from jobs.models import Job
from applications.models import Application
from profiles.models import Company
from datetime import date

User = get_user_model()

@login_required
@seeker_required
def seeker_dashboard_view(request):
    user = request.user
    applications = Application.objects.filter(job_seeker=user)
    
    total_applied = applications.count()
    under_review = applications.filter(status='Under Review').count()
    shortlisted = applications.filter(status='Shortlisted').count()
    selected = applications.filter(status='Selected').count()
    rejected = applications.filter(status='Rejected').count()
    
    recent_applications = applications.order_by('-applied_at')[:5]
    
    context = {
        'total_applied': total_applied,
        'under_review': under_review,
        'shortlisted': shortlisted,
        'selected': selected,
        'rejected': rejected,
        'recent_applications': recent_applications,
    }
    return render(request, 'dashboards/seeker_dashboard.html', context)

@login_required
@recruiter_required
def recruiter_dashboard_view(request):
    user = request.user
    posted_jobs = Job.objects.filter(recruiter=user)
    
    total_posted = posted_jobs.count()
    active_jobs = posted_jobs.filter(status='approved', deadline__gte=date.today()).count()
    
    # An expired job is either closed or the deadline has passed
    expired_jobs = posted_jobs.filter(status='closed').count() + posted_jobs.filter(deadline__lt=date.today()).exclude(status='closed').count()
    
    # Applications to recruiter's jobs
    recruiter_applications = Application.objects.filter(job__recruiter=user)
    total_applications = recruiter_applications.count()
    
    shortlisted = recruiter_applications.filter(status__in=['Shortlisted', 'Interview']).count()
    selected = recruiter_applications.filter(status='Selected').count()
    
    recent_applications = recruiter_applications.order_by('-applied_at')[:5]
    
    # Statistics for JS chart (applications per job)
    job_stats = []
    for job in posted_jobs[:5]:
        job_stats.append({
            'title': job.title[:15] + '...' if len(job.title) > 15 else job.title,
            'count': job.applications.count()
        })
        
    context = {
        'total_posted': total_posted,
        'active_jobs': active_jobs,
        'expired_jobs': expired_jobs,
        'total_applications': total_applications,
        'shortlisted_candidates': shortlisted,
        'selected_candidates': selected,
        'recent_applications': recent_applications,
        'job_stats': job_stats,
    }
    return render(request, 'dashboards/recruiter_dashboard.html', context)

@login_required
@admin_required
def admin_dashboard_view(request):
    total_users = User.objects.count()
    total_seekers = User.objects.filter(role='job_seeker').count()
    total_recruiters = User.objects.filter(role='recruiter').count()
    total_companies = Company.objects.count()
    total_jobs = Job.objects.count()
    total_applications = Application.objects.count()
    
    # Recent items
    recent_jobs = Job.objects.order_by('-created_at')[:5]
    recent_users = User.objects.order_by('-date_joined')[:5]
    
    context = {
        'total_users': total_users,
        'total_seekers': total_seekers,
        'total_recruiters': total_recruiters,
        'total_companies': total_companies,
        'total_jobs': total_jobs,
        'total_applications': total_applications,
        'recent_jobs': recent_jobs,
        'recent_users': recent_users,
    }
    return render(request, 'dashboards/admin_dashboard.html', context)
