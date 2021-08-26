from django.urls import path
from blog import views
urlpatterns = [
    # API for comment
    path('postComment', views.postComment, name="postComment"),
    # rest urls
    path('', views.blogHome, name='blogHome'),
    # slug url for all posts
    path('<str:slug>', views.blogPost, name='blogPost'),
    #path('post/like/', views.like, name='like-post'),
]