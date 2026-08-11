from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import seeker_required, recruiter_required
from .models import JobSeekerProfile, RecruiterProfile, Company
from .forms import UserUpdateForm, JobSeekerProfileForm, RecruiterProfileForm, CompanyForm

# Helper to custom handle get_object_or_404 for clarity
def get_object_or_ok(klass, *args, **kwargs):
    return get_object_or_404(klass, *args, **kwargs)

@login_required
@seeker_required
def seeker_profile_view(request):
    profile, created = JobSeekerProfile.objects.get_or_create(user=request.user)
    return render(request, 'profiles/seeker_profile.html', {'profile': profile})

@login_required
@seeker_required
def edit_seeker_profile(request):
    profile, created = JobSeekerProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = JobSeekerProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('seeker_profile')
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = JobSeekerProfileForm(instance=profile)
        
    return render(request, 'profiles/edit_seeker.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
@recruiter_required
def recruiter_profile_view(request):
    profile, created = RecruiterProfile.objects.get_or_create(user=request.user)
    return render(request, 'profiles/recruiter_profile.html', {'profile': profile})

@login_required
@recruiter_required
def edit_recruiter_profile(request):
    profile, created = RecruiterProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = RecruiterProfileForm(request.POST, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile details have been updated!")
            return redirect('recruiter_profile')
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = RecruiterProfileForm(instance=profile)
        
    return render(request, 'profiles/edit_recruiter.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
@recruiter_required
def manage_company_view(request):
    # Recruiter can manage the company they are associated with or create one
    profile, created = RecruiterProfile.objects.get_or_create(user=request.user)
    company = profile.company
    
    if request.method == 'POST':
        if company:
            form = CompanyForm(request.POST, request.FILES, instance=company)
        else:
            form = CompanyForm(request.POST, request.FILES)
            
        if form.is_valid():
            company_obj = form.save(commit=False)
            company_obj.recruiter = request.user
            company_obj.save()
            
            # Associate company with recruiter
            profile.company = company_obj
            profile.save()
            
            messages.success(request, "Company profile saved successfully!")
            return redirect('recruiter_profile')
        else:
            messages.error(request, "Failed to save company profile. Check your input.")
    else:
        if company:
            form = CompanyForm(instance=company)
        else:
            form = CompanyForm()
            
    return render(request, 'profiles/company_profile.html', {'form': form, 'company': company})

def company_detail_view(request, company_id):
    company = get_object_or_ok(Company, id=company_id)
    # Get active jobs for this company
    jobs = company.jobs.filter(status='approved')
    return render(request, 'profiles/company_detail.html', {'company': company, 'jobs': jobs})
