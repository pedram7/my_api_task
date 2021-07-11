"""my_api_task URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/create_post/', login_required(PostView.as_view(), login_url='/api/login/'), name='create_post'),
    path('api/update_post/', login_required(PostView.as_view(), login_url='/api/login/'), name='update_post'),
    path('api/delete_post/', login_required(PostView.as_view(), login_url='/api/login/'), name='delete_post'),
    path('api/create_comment/', login_required(CommentView.as_view(), login_url='/api/login/'), name='create_comment'),
    path('api/delete_comment/', login_required(CommentView.as_view(), login_url='/api/login/'), name='delete_comment'),
    path('api/like_post/', login_required(like_post, login_url='/api/login/'), name='like_post'),
    path('api/dislike_post/', login_required(dislike_post, login_url='/api/login/'), name='dislike_post'),
    path('api/like_comment/', login_required(like_comment, login_url='/api/login/'), name='like_comment'),
    path('api/dislike_comment/', login_required(dislike_comment, login_url='/api/login/'), name='dislike_comment'),

    path('api/is_post_edited/', is_edited, name='is_edited'),
]
