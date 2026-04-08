from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.conf import settings
from .models import LeaveRequest
from .forms import LeaveRequestForm

class LeaveRequestListView(LoginRequiredMixin, ListView):
    model = LeaveRequest
    template_name = 'leaves/request_list.html'
    context_object_name = 'requests'
    ordering = ['-leave_date']

class LeaveRequestCreateView(LoginRequiredMixin, CreateView):
    model = LeaveRequest
    form_class = LeaveRequestForm
    template_name = 'leaves/request_form.html'
    success_url = reverse_lazy('request_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Send Email Notification
        subject = f"New Leave Request: {self.object.student_name}"
        message = f"A new leave request has been submitted by {self.object.student_name} for {self.object.leave_date}.\n\nReason: {self.object.reason}"
        from_email = settings.DEFAULT_FROM_EMAIL or 'noreply@leaveflow.com'
        recipient_list = [admin[1] for admin in settings.ADMINS] if settings.ADMINS else ['admin@example.com']
        
        try:
            send_mail(subject, message, from_email, recipient_list)
        except Exception as e:
            print(f"Failed to send email: {e}")
            
        return response

class LeaveRequestUpdateView(LoginRequiredMixin, UpdateView):
    model = LeaveRequest
    form_class = LeaveRequestForm
    template_name = 'leaves/request_form.html'
    success_url = reverse_lazy('request_list')

class LeaveRequestDeleteView(LoginRequiredMixin, DeleteView):
    model = LeaveRequest
    template_name = 'leaves/request_confirm_delete.html'
    success_url = reverse_lazy('request_list')
