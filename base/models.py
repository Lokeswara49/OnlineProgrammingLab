from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    # participants=
    verified = models.BooleanField(default=False)
    room_password = models.CharField(max_length=20, default="admin123")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Question(models.Model):
    question_title = models.CharField(max_length=50)
    question_full = models.TextField()
    sample_test_case = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_title


# Model for solution
class Solution(models.Model):
    code = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    input = models.TextField(null=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user

class VerifiedUser(models.Model):
    is_verified = models.BooleanField(default=False)
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
# refer this for User model and its attributes -- https://docs.djangoproject.com/en/4.0/ref/contrib/auth/
