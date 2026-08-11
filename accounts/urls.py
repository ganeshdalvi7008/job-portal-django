from django.urls import path
from . import views, dashboards

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/seeker/', views.seeker_register, name='seeker_register'),
    path('register/recruiter/', views.recruiter_register, name='recruiter_register'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('dashboard-redirect/', views.dashboard_redirect, name='dashboard_redirect'),
    
    # Dashboards
    path('seeker/dashboard/', dashboards.seeker_dashboard_view, name='seeker_dashboard'),
    path('recruiter/dashboard/', dashboards.recruiter_dashboard_view, name='recruiter_dashboard'),
    path('admin/dashboard/', dashboards.admin_dashboard_view, name='admin_dashboard'),
]
