from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class Profile(models.Model):
    profile_user=models.OneToOneField(User,on_delete=models.CASCADE)
    address=models.TextField()
    profile_pic=models.ImageField(upload_to='abcd')

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    study_hours = models.FloatField()
    play_hours = models.FloatField()
    sleep_hours = models.FloatField()
    tv_hours = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    image = models.FileField(upload_to='chart/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"