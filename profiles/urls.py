from django.urls import path
from . import views

urlpatterns = [
    path('seeker/profile/', views.seeker_profile_view, name='seeker_profile'),
    path('seeker/profile/edit/', views.edit_seeker_profile, name='edit_seeker_profile'),
    path('recruiter/profile/', views.recruiter_profile_view, name='recruiter_profile'),
    path('recruiter/profile/edit/', views.edit_recruiter_profile, name='edit_recruiter_profile'),
    path('recruiter/company/manage/', views.manage_company_view, name='manage_company'),
    path('company/<int:company_id>/', views.company_detail_view, name='company_detail'),
]
