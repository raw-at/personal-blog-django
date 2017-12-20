from django.contrib import admin

# Register your models here.

#Used to setup our Post app with the admin panel
from .models import Post


#admin function to register model with admin site
admin.site.register(Post)
