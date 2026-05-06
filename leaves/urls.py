from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='request_list'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('new/', views.LeaveRequestCreateView.as_view(), name='request_create'),
    path('<int:pk>/edit/', views.LeaveRequestUpdateView.as_view(), name='request_update'),
    path('<int:pk>/delete/', views.LeaveRequestDeleteView.as_view(), name='request_delete'),
    path('<int:pk>/approve/', views.approve_leave, name='approve_leave'),
    path('<int:pk>/reject/', views.reject_leave, name='reject_leave'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path('my-requests/', views.MyRequestsListView.as_view(), name='my_requests'),
    path('all-requests/', views.LeaveRequestListView.as_view(), name='all_requests'),
    path('analytics/', views.AdminAnalyticsView.as_view(), name='analytics'),
    path('api/events/', views.leave_events, name='leave_events'),
]
