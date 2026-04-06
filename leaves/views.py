from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import LeaveRequest
from .forms import LeaveRequestForm

class LeaveRequestListView(ListView):
    model = LeaveRequest
    template_name = 'leaves/request_list.html'
    context_object_name = 'requests'
    ordering = ['-leave_date']

class LeaveRequestCreateView(CreateView):
    model = LeaveRequest
    form_class = LeaveRequestForm
    template_name = 'leaves/request_form.html'
    success_url = reverse_lazy('request_list')

class LeaveRequestUpdateView(UpdateView):
    model = LeaveRequest
    form_class = LeaveRequestForm
    template_name = 'leaves/request_form.html'
    success_url = reverse_lazy('request_list')

class LeaveRequestDeleteView(DeleteView):
    model = LeaveRequest
    template_name = 'leaves/request_confirm_delete.html'
    success_url = reverse_lazy('request_list')
