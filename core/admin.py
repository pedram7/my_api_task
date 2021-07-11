from django.contrib import admin

# Register your models here.
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'last_name', 'last_login')
    readonly_fields = ['id', 'last_login']


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'posted_time')
    readonly_fields = ['id', 'posted_time', 'last_edited']


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'comment_time')
    readonly_fields = ['id', 'comment_time']


admin.site.register(BlogUser, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
