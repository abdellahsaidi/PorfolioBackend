from django.db import models


class CV(models.Model):
    file = models.FileField(upload_to='cv/', blank=False, null=False)

    def save(self, *args, **kwargs):
        if CV.objects.exists() and not self.pk:
            raise ValueError("There can only be one CV instance.")
        super(CV, self).save(*args, **kwargs)

    def __str__(self):
        return "My CV"


class SendMail(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200)   
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - from {self.full_name} ({self.email})"
