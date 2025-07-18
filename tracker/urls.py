from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('start-drive/', views.start_drive, name='start_drive'),
    path('drive/<int:session_id>/', views.drive_route, name='drive_route'),
    path('rider-info/', views.rider_info, name='rider_info'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
]

