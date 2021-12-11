from django.db import models
from django.core.validators import MinLengthValidator
from .uniqueslug import unique_slug_generator
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.contrib.auth.models import User


# Create your models here.

class Author(models.Model):

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Tag(models.Model):
    captions = models.CharField(max_length=30)

    def __str__(self):
        return self.captions 

class Post(models.Model):
    title = models.CharField(max_length=60)
    excerpt = models.CharField(max_length=300)
    image = models.ImageField(upload_to="posts",null=True)
    date = models.DateField(auto_now=True)
    slug = models.SlugField(unique=True)
    content = models.TextField(validators=[MinLengthValidator(10)])
    author = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title

@receiver(pre_save, sender=Post)
def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
pre_save.connect(slug_generator,sender=Post)



class Comment(models.Model):
    user_name = models.CharField(max_length=50)
    email = models.EmailField()
    text = models.TextField(max_length=400)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,null=True,related_name='comments')



