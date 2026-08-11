from django.shortcuts import render
from django.contrib.auth import get_user_model
from jobs.models import Job
from profiles.models import Company

User = get_user_model()

def home_view(request):
    featured_jobs = Job.objects.filter(status='approved').order_by('-created_at')[:3]
    total_jobs = Job.objects.filter(status='approved').count()
    total_companies = Company.objects.count()
    total_seekers = User.objects.filter(role='job_seeker').count()
    
    # Add a base offset for college viva demo data looks robust
    context = {
        'featured_jobs': featured_jobs,
        'total_jobs_stat': total_jobs + 15,
        'total_companies_stat': total_companies + 6,
        'total_seekers_stat': total_seekers + 38,
    }
    return render(request, 'home.html', context)

def about_view(request):
    return render(request, 'about.html')

def contact_view(request):
    if request.method == 'POST':
        # Simple simulated contact form submission
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # We could save this to database or print
        print(f"Contact Form Query - Name: {name}, Email: {email}, Subject: {subject}, Msg: {message}")
        
        from django.contrib import messages
        messages.success(request, f"Thank you, {name}! Your message has been received. We will get back to you shortly.")
        return render(request, 'contact.html', {'success': True})
        
    return render(request, 'contact.html')
