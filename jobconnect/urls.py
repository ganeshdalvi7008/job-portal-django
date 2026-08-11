from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),
    
    # Root Public Pages
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    
    # Application App Routers
    path('accounts/', include('accounts.urls')),
    path('profiles/', include('profiles.urls')),
    path('jobs/', include('jobs.urls')),
    path('applications/', include('applications.urls')),
]

# Serve Static and Media uploads in Development mode
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
