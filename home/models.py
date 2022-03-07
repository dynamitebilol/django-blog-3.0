from django.db import models
from django.contrib.auth.models import User
from django.db.models import TextField
from froala_editor.fields import FroalaField
from .helpers import generate_slug
from django.utils import timezone


class BlogModel(models.Model):
    title = models.CharField(max_length=500)
    content = FroalaField()
    slug = models.SlugField(max_length=500, null=True, blank=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog')
    created_at = models.DateTimeField(auto_now_add=True)
    upload_to = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.title)
        super(BlogModel, self).save(*args, **kwargs)

    @property
    def number_of_comments(self):
        return BlogComment.objects.filter(blogpost_connected=self).count()

    def number_of_likes(self):
        return self.likes.count()


class BlogComment(models.Model):
    blogpost_connected = models.ForeignKey(
        BlogModel, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.author) + ', ' + self.blogpost_connected.title[:40]