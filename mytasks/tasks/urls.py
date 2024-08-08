from django.urls import path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    AddTaskView,
    CheckAuthenticationView,
    ListTaskView,
    LogoutView,
    MyTokenObtainPairView,
    RegisterView,
    TaskDeleteView,
    TaskSearchView,
)

urlpatterns = [
    #landing page
    path('dashboard/', TemplateView.as_view(template_name='tasks/home.html'), name='dashboard'),
    path('', CheckAuthenticationView.as_view(), name='home'),
    
    
    #register page
    path('register/', TemplateView.as_view(template_name='tasks/register.html'), name='register'),
    path('event/register/', RegisterView.as_view(), name='api_register'),
    
    #login page
    path('login/', TemplateView.as_view(template_name='tasks/login.html'), name='login'),
    path('event/login/', MyTokenObtainPairView.as_view(), name='api_login'),     
    
    #other
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('tasks/add/', AddTaskView.as_view(), name='add_task'),
    path('tasks/', ListTaskView.as_view(), name='list_tasks'),
    path('tasks/search/', TaskSearchView.as_view(), name='task_search'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
]

