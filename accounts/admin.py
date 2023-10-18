from django.contrib import admin
from .models import CustomUser, NewsLetterSubcribers

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(NewsLetterSubcribers)
