from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SeekerRegistrationForm, RecruiterRegistrationForm
from django.contrib.auth import get_user_model

User = get_user_model()

def seeker_register(request):
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')
        
    if request.method == 'POST':
        form = SeekerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Registration successful! You can now login.")
            return redirect('login')
        else:
            messages.error(request, "Registration failed. Please check the fields below.")
    else:
        form = SeekerRegistrationForm()
        
    return render(request, 'accounts/register.html', {'form': form, 'role': 'Job Seeker'})

def recruiter_register(request):
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')
        
    if request.method == 'POST':
        form = RecruiterRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Registration successful! You can now login.")
            return redirect('login')
        else:
            messages.error(request, "Registration failed. Please check the fields below.")
    else:
        form = RecruiterRegistrationForm()
        
    return render(request, 'accounts/register.html', {'form': form, 'role': 'Recruiter'})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name}!")
                return redirect('dashboard_redirect')
            else:
                messages.error(request, "This account is inactive. Please contact the administrator.")
        else:
            messages.error(request, "Invalid username or password.")
            
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')

@login_required
def dashboard_redirect(request):
    if request.user.is_superuser or request.user.role == 'admin':
        return redirect('admin_dashboard')
    elif request.user.role == 'recruiter':
        return redirect('recruiter_dashboard')
    else:
        return redirect('seeker_dashboard')

def forgot_password_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        try:
            user = User.objects.get(username=username, email=email)
            # Simulated reset for demo/viva ease
            temp_pass = "Reset@123"
            user.set_password(temp_pass)
            user.save()
            messages.success(
                request, 
                f"Password reset successful! Use temporary password: '{temp_pass}' to login and change your password."
            )
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, "No user found with the matching username and email.")
            
    return render(request, 'accounts/forgot_password.html')

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            messages.success(request, "Your password was successfully updated!")
            return redirect('dashboard_redirect')
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordChangeForm(request.user)
        
    for field in form.fields.values():
        field.widget.attrs.update({'class': 'form-control'})
        
    return render(request, 'accounts/change_password.html', {'form': form})
