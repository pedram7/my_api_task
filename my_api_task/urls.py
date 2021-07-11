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
    path('api/register/', RegisterView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='login'),
    path('api/create_post/', PostView.as_view(), name='login'),
    path('api/update_post/', PostView.as_view(), name='login'),
    path('api/delete_post/', PostView.as_view(), name='login'),
    path('api/create_comment/', CommentView.as_view(), name='login'),
    path('api/delete_comment/', CommentView.as_view(), name='login'),
    # path('api/like_post', LoginView.as_view(), name='login'),
    # path('api/dislike_post', LoginView.as_view(), name='login'),
    # path('api/like_comment', LoginView.as_view(), name='login'),
    # path('api/dislike_comment', LoginView.as_view(), name='login'),

    path('is_post_edited', LoginView.as_view(), name='login'),
]
