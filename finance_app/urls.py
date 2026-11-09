from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='finance_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('expenses/', views.expense_list_view, name='expense_list'),
    path('expenses/add/', views.expense_add_view, name='expense_add'),
    path('ai-insights/', views.ai_insights_view, name='ai_insights'),
    path('reports/', views.reports_view, name='reports'),
]
