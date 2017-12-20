from django.db import models

# Create your models here.


#Post model created with four fields
class Post(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add = True,auto_now = False)
    updated = models.DateTimeField(auto_now_add = False,auto_now = True)


    def __str__(self):
        return self.title
