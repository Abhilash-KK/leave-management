from django.db import models
from django.contrib.auth.models import User

class LeaveRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leave_requests')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True, help_text="Optional for single day leave")
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    attachment = models.FileField(upload_to='leaves/attachments/', null=True, blank=True, help_text="Upload a medical certificate or proof (Optional)")
    admin_response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.start_date}"

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    college_name = models.CharField(max_length=200, blank=True)
    department = models.CharField(max_length=100, blank=True)
    registration_number = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"Profile for {self.user.username}"

# Signals to automatically create/save student profile
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created and not instance.is_staff:
        StudentProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_student_profile(sender, instance, **kwargs):
    if not instance.is_staff and hasattr(instance, 'profile'):
        instance.profile.save()
