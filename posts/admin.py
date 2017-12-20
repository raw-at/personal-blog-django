from django.contrib import admin

# Register your models here.

#Used to setup our Post app with the admin panel
from .models import Post

class PostModelAdmin(admin.ModelAdmin):

    list_display = ['title','updated','timestamp']
    list_display_links = ['updated']
    list_filter = ['title']
    search_fields = ['title','content']
    class Meta:
        model = Post


#admin function to register model with admin site
admin.site.register(Post,PostModelAdmin)
