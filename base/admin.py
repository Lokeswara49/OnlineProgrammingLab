from django.contrib import admin

# Register your models here.

from .models import Room, Question, Solution, VerifiedUser

admin.site.register(Room)
admin.site.register(Question)
admin.site.register(Solution)
admin.site.register(VerifiedUser)
