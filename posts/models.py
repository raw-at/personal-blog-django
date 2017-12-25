from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils import timezone
from django.conf import settings
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType

from markdown_deux import markdown
# Create your models here.

#Example of Model Manager
#Post.objects.all()
from comments.models import Comment
from .utils import get_read_time

class PostManager(models.Manager):
    def active(self,*args,**kwrags):
        return super(PostManager,self).filter(draft=False).filter(publish__lte=timezone.now())


def upload_location(instance,filename):
    return "%s/%s" %(instance.id,filename)


#Post model created with four fields
class Post(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
    image = models.ImageField(upload_to=upload_location,
            null=True,
            blank=True,
            width_field="width_field",
            height_field="height_field")

    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)
    draft =  models.BooleanField(default=True)
    publish = models.DateField(auto_now=False , auto_now_add=False)
    read_time = models.TimeField(null=True,blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add = True,auto_now = False)
    updated = models.DateTimeField(auto_now_add = False,auto_now = True)

    objects = PostManager()
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:detail',kwargs={"slug":self.slug})

    def get_markdown(self):
        content = self.content
        return mark_safe(markdown(content))
    class Meta:
        ordering = ["-timestamp",'-updated']

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type


def create_slug(instance,new_slug = None):
    slug = slugify(instance.title)  #abc123 -> abc-123 this is slug that's it
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug,qs.first().id)
        return create_slug(instance,new_slug = new_slug)
    return slug



def pre_save_post_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
    if instance.content:
        read_time = get_read_time(instance.get_markdown())
        instance.read_time = read_time

pre_save.connect(pre_save_post_receiver,sender=Post)
