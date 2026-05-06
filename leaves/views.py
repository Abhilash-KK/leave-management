from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login
from django.core.mail import send_mail
from django.conf import settings
from .models import LeaveRequest, StudentProfile
from .forms import LeaveRequestForm, StudentRegistrationForm, UserUpdateForm, StudentProfileForm
from django.contrib import messages

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'leaves/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_staff:
            base_qs = LeaveRequest.objects.all()
        else:
            base_qs = LeaveRequest.objects.filter(user=user)
            
        context['total_count'] = base_qs.count()
        context['approved_count'] = base_qs.filter(status='Approved').count()
        context['pending_count'] = base_qs.filter(status='Pending').count()
        context['rejected_count'] = base_qs.filter(status='Rejected').count()
        context['is_admin'] = user.is_staff
        return context

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = StudentProfile
    form_class = StudentProfileForm
    template_name = 'leaves/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        profile, created = StudentProfile.objects.get_or_create(user=self.request.user)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['user_form'] = UserUpdateForm(self.request.POST, instance=self.request.user)
            context['profile_form'] = StudentProfileForm(self.request.POST, instance=self.get_object())
        else:
            context['user_form'] = UserUpdateForm(instance=self.request.user)
            context['profile_form'] = StudentProfileForm(instance=self.get_object())
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']
        if user_form.is_valid() and form.is_valid():
            user_form.save()
            form.save()
            messages.success(self.request, "Profile updated successfully!")
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class MyRequestsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = LeaveRequest
    template_name = 'leaves/request_list.html'
    context_object_name = 'requests'

    def test_func(self):
        return not self.request.user.is_staff

    def get_queryset(self):
        return LeaveRequest.objects.filter(user=self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = False
        context['header_title'] = "My Leave Requests"
        return context

class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = StudentRegistrationForm
    success_url = reverse_lazy('request_list')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Account created! Welcome to Student Leave Hub.")
        return redirect(self.success_url)

class LeaveRequestListView(LoginRequiredMixin, ListView):
    model = LeaveRequest
    template_name = 'leaves/request_list.html'
    context_object_name = 'requests'

    def get_queryset(self):
        if self.request.user.is_staff:
            return LeaveRequest.objects.all().order_by('-created_at')
        return LeaveRequest.objects.filter(user=self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = self.request.user.is_staff
        return context

class LeaveRequestCreateView(LoginRequiredMixin, CreateView):
    model = LeaveRequest
    form_class = LeaveRequestForm
    template_name = 'leaves/request_form.html'
    success_url = reverse_lazy('request_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        
        # Send Email Notification
        subject = f"New Leave Request: {self.request.user.username}"
        message = f"A new leave request has been submitted by {self.request.user.username} from {self.object.start_date} to {self.object.end_date or 'N/A'}.\n\nReason: {self.object.reason}"
        from_email = settings.DEFAULT_FROM_EMAIL or 'noreply@studentleavehub.com'
        recipient_list = [admin[1] for admin in settings.ADMINS] if settings.ADMINS else ['admin@example.com']
        
        try:
            send_mail(subject, message, from_email, recipient_list)
        except Exception as e:
            print(f"Failed to send email: {e}")
            
        messages.success(self.request, "Leave request submitted successfully!")
        return response

def approve_leave(request, pk):
    if not request.user.is_staff:
        return redirect('request_list')
    leave = get_object_or_404(LeaveRequest, pk=pk)
    leave.status = 'Approved'
    leave.admin_response = request.POST.get('admin_response', '')
    leave.save()
    messages.success(request, f"Leave request for {leave.user.username} approved.")
    return redirect('request_list')

def reject_leave(request, pk):
    if not request.user.is_staff:
        return redirect('request_list')
    leave = get_object_or_404(LeaveRequest, pk=pk)
    leave.status = 'Rejected'
    leave.admin_response = request.POST.get('admin_response', '')
    leave.save()
    messages.error(request, f"Leave request for {leave.user.username} rejected.")
    return redirect('request_list')

class LeaveRequestUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = LeaveRequest
    form_class = LeaveRequestForm
    template_name = 'leaves/request_form.html'
    success_url = reverse_lazy('request_list')

    def test_func(self):
        leave = self.get_object()
        return self.request.user == leave.user and leave.status == 'Pending'

class LeaveRequestDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = LeaveRequest
    template_name = 'leaves/request_confirm_delete.html'
    success_url = reverse_lazy('request_list')

    def test_func(self):
        leave = self.get_object()
        if self.request.user.is_staff:
            return leave.status == 'Rejected'
        return self.request.user == leave.user and leave.status == 'Pending'
