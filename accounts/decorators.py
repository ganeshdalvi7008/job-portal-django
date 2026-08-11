from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied

def seeker_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Please login as a Job Seeker to access this page.")
            return redirect('login')
        if request.user.role != 'job_seeker':
            messages.error(request, "Access denied. Only Job Seekers are allowed here.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper

def recruiter_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Please login as a Recruiter to access this page.")
            return redirect('login')
        if request.user.role != 'recruiter':
            messages.error(request, "Access denied. Only Recruiters are allowed here.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Please login to access this page.")
            return redirect('login')
        if request.user.role != 'admin' and not request.user.is_superuser:
            messages.error(request, "Access denied. Admin privileges required.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper
