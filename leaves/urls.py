from django.urls import path
from . import views

urlpatterns = [
    path('', views.LeaveRequestListView.as_view(), name='request_list'),
    path('new/', views.LeaveRequestCreateView.as_view(), name='request_create'),
    path('<int:pk>/edit/', views.LeaveRequestUpdateView.as_view(), name='request_update'),
    path('<int:pk>/delete/', views.LeaveRequestDeleteView.as_view(), name='request_delete'),
]
