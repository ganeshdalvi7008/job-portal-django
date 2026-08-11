from django.urls import path
from . import views

urlpatterns = [
    path('apply/<int:job_id>/', views.apply_job_view, name='apply_job'),
    path('my-applications/', views.my_applications_view, name='my_applications'),
    path('detail/<int:app_id>/', views.application_detail_view, name='application_detail'),
    path('update-status/<int:app_id>/', views.update_application_status_view, name='update_application_status'),
    path('job/<int:job_id>/applicants/', views.job_applicants_view, name='job_applicants'),
    path('download-resume/<int:app_id>/', views.download_resume_view, name='download_resume'),
]
