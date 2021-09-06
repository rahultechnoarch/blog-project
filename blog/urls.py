from django.urls import path
from blog import views
from django.views.generic import TemplateView

urlpatterns = [
    path('related', views.related, name='related'),
    
    path('createPost', views.PostCreateView.as_view(), name='post-create-view'),
    # API for posting comment
    path('PostComment', views.PostCommentView.as_view(), name="post-comment-view"),
    
    #path('/deletepost', views.PostDeleteView.as_view(), name='post-delete-view'),
    # slug url for all posts
    path('<str:slug>', views.BlogPostView.as_view(), name='blogpost-view'),
    
    # lists all the posts
    path('', views.PostListView.as_view(), name='post-list-view'),
    
]