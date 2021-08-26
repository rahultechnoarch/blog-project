from typing import ContextManager
from django.shortcuts import redirect, render, HttpResponse, get_object_or_404
from blog.models import Post, BlogComment
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse

# Create your views here.
# homepage ref
def blogHome(request):
    allPosts = Post.objects.all()
    context = {'allPosts': allPosts}
    return render(request, 'blog/blogHome.html', context)

# post ref
def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    # for couting post views
    post.views = post.views + 1
    post.save()

    comments = BlogComment.objects.filter(post=post, parent=None)
    # reply api
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]            
        else:
            replyDict[reply.parent.sno].append(reply)

    context = {'post': post, 'comments': comments, 'user': request.user, 'replyDict': replyDict}
    return render(request, 'blog/blogPost.html', context)

# comment post ref
def postComment(request):
    if request.method == "POST":
        comment = request.POST.get("comment")
        user = request.user
        postSno = request.POST.get("postSno")
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST.get("parentSno")
        if parentSno == "":
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request, "Comment posted successfully")

        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment, user=user, post=post, parent=parent)
            comment.save()
            messages.success(request, "Reply posted successfully")

    return redirect(f"/blog/{post.slug}")

'''
def like(request):
    post_id = request.POST['post_id']
    post = Post.objects.get(pk=post_id)
    liked = True

    like_object, created = Like.objects.get_or_create(user_id = request.user, post_id = post)
    if not created:
        like_object.delete() # the user already liked this picture before
        liked = False
    
    return JsonResponse({'liked':liked}) 

def posts(request):
    posts = Post.objects.all()
    liked_posts = []
    
    for liked_post in request.user.likes.all(): # likes is the related name used in models
        liked_posts.append(liked_post.post_id)

    return render(request, 'home.html', {'posts':posts, 'liked_posts':liked_posts})
''' 