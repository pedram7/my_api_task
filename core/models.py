from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
import core


class BlogUser(AbstractUser):
    biography = models.CharField(max_length=255)

    def __str__(self):
        return "{} {}({})".format(self.first_name, self.last_name, self.username)


class Post(models.Model):
    text = models.TextField()
    likes = models.ManyToManyField(BlogUser, related_name='liked_posts', blank=True, null=True)
    dislikes = models.ManyToManyField(BlogUser, related_name='disliked_posts', null=True, blank=True)
    user = models.ForeignKey(BlogUser, related_name='posts', on_delete=models.CASCADE)
    posted_time = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    parent_comment = models.ForeignKey(core.models.Comment, on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    likes = models.ManyToManyField(BlogUser, related_name='liked_posts', blank=True, null=True)
    dislikes = models.ManyToManyField(BlogUser, related_name='disliked_posts', blank=True, null=True)
    user = models.ForeignKey(BlogUser, related_name='comments', on_delete=models.CASCADE)
    comment_time = models.DateTimeField(auto_now_add=True)
