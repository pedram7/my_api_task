from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class BlogUser(AbstractUser):
    biography = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "{} {}({})".format(self.first_name, self.last_name, self.username)


class Post(models.Model):
    text = models.TextField()
    likes = models.ManyToManyField(BlogUser, related_name='liked_posts', blank=True)
    dislikes = models.ManyToManyField(BlogUser, related_name='disliked_posts', blank=True)
    user = models.ForeignKey(BlogUser, related_name='posts', on_delete=models.CASCADE)
    posted_time = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} post:{}...".format(self.user, self.text[:max(20, len(self.text))])


class Comment(models.Model):
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    likes = models.ManyToManyField(BlogUser, related_name='liked_comments', blank=True)
    dislikes = models.ManyToManyField(BlogUser, related_name='disliked_comments', blank=True)
    user = models.ForeignKey(BlogUser, related_name='comments', on_delete=models.CASCADE)
    comment_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} comment:{}...".format(self.user, self.text[:max(20, len(self.text))])
