from django.db import models

class LeaveRequest(models.Model):
    student_name = models.CharField(max_length=100)
    leave_date = models.DateField()
    reason = models.TextField()

    def __str__(self):
        return f"{self.student_name} - {self.leave_date}"
