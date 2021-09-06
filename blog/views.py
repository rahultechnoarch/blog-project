from collections import namedtuple
from django.shortcuts import redirect, render, HttpResponse, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy, reverse
# import important views
from django.views.generic.list import ListView
from django.views.generic import View, TemplateView, CreateView, UpdateView, DeleteView, DetailView
# import all the models (from all apps)
from blog.models import Post, BlogComment
from blog.forms import PostForm

def related(request):
    return render(request, 'home/relatedvideos.html')
    
# views start from here
class PostCreateView(CreateView):
    model = Post
    def get(self, request):
        form = PostForm()
        context = {'form': form}
        return render(request, 'blog/createPost.html', context)
    
    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/blog/')

# list all available posts
class PostListView(ListView):
    model = Post
    template_name = 'blogHome.html'
    context_object_name = 'allPosts'

# Post Blog
class BlogPostView(View):
    def post(self, request):
        pass

    def get(self, request, slug):
        post = Post.objects.filter(slug=slug).first()
        # for couting post views
        post.views = post.views + 1
        post.save()

        comments = BlogComment.objects.filter(post=post, parent=None)
        # reply comment api
        replies = BlogComment.objects.filter(post=post).exclude(parent=None)
        replyDict = {}
        for reply in replies:
            if reply.parent.sno not in replyDict.keys():
                replyDict[reply.parent.sno] = [reply]            
            else:
                replyDict[reply.parent.sno].append(reply)
        context = {'post': post, 'comments': comments, 'user': request.user, 'replyDict': replyDict}
        return render(request, 'blog/blogPost.html', context)

# Post comment
class PostCommentView(View):
    def post(self, request):
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
        
    def get(self, request, slug):
        postSno = request.POST.get("postSno")
        post = Post.objects.get(sno=postSno)
        return redirect(f"/blog/{post.slug}")



#class PostUpdate(UpdateView):
#    model = Post
#   fields = ['tile', 'author', 'content']
#   success_url = reverse_lazy('posts')

#class PostDeleteView(DeleteView):
#    model = Post
#    context_object_name = 'allPosts'
#    success_url = reverse_lazy('blog/blogPost.html')