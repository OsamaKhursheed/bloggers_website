from django.db import models

class blog_maker(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    profile_image = models.ImageField(upload_to='user_profiles/', null=True, blank=True)
    father_name = models.CharField(max_length=255)
    email = models.EmailField()
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    status= models.BooleanField(default=False)