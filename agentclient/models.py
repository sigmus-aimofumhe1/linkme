from django.db import models

# Create your models here.

# Added by Sigmus
class Contact(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    context = models.TextField(null=True, blank=True)  # where you met or notes
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name or self.email or self.phone or "Unknown Contact"
