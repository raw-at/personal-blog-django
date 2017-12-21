from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.


#Post model created with four fields
class Post(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add = True,auto_now = False)
    updated = models.DateTimeField(auto_now_add = False,auto_now = True)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:detail',kwargs={"id":self.id})

        #return "/posts/%s" %(self.id) <--------------- HARD CODED
    class Meta:
        ordering = ["-timestamp",'-updated']
