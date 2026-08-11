from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list_view, name='job_list'),
    path('<int:job_id>/', views.job_detail_view, name='job_detail'),
    path('add/', views.add_job_view, name='add_job'),
    path('<int:job_id>/edit/', views.edit_job_view, name='edit_job'),
    path('<int:job_id>/delete/', views.delete_job_view, name='delete_job'),
    path('manage/', views.manage_jobs_view, name='manage_jobs'),
]
