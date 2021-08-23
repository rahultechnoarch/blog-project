from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from blog.models import Post
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
# Create your views here.
#HTML pages
def home(request):
    return render(request, 'home/home.html')

def about(request):
    return render(request, 'home/about.html')

#contact form ref
def contact(request):
    if request.method=='POST':
        #get all contact form parameters
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        print(name, email, phone, content)

        if len(name)<3 or len(email)<8 or len(phone)<5:
            messages.error(request, "Please fill the form correctly")
        else:
            contact= Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Your message has been sent.")
    return render(request, 'home/contact.html')

# search ref using title, content
def search(request):
    searchquery = request.GET['searchquery']
    if len(searchquery)>50:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=searchquery)
        allPostsContent = Post.objects.filter(content__icontains=searchquery)
        allPosts = allPostsTitle.union(allPostsContent)

    if allPosts.count() == 0:
        messages.warning(request, "No related articles found")
    params = {'allPosts': allPosts, 'searchquery': searchquery}
    return render(request, 'home/search.html', params)

#APIs
def signuphandle(request):
    if request.method == 'POST':
        #get all signup form parameters
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        #check signup username and password validity
        if not username.isalnum():
            messages.error(request, "Alpha-Numeric Username only.")
            return redirect('home')
        if len(username) > 15:
            messages.error(request, "Username must be under 15 characters.")
            return redirect('home')
        if password1 != password2:
            messages.error(request, "Password do not match.")
            return redirect('home')

        #create user after validation
        myuser = User.objects.create_user(username, email, password1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "You've successfully created your account")
        return redirect('home')
    else:
        return HttpResponse('404 - Not Found')
 
def loginhandle(request):
    if request.method == 'POST':
        #get all login form parameters
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "You're logged in")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials, Try again")
            return redirect('home')

    return HttpResponse('404 - Not Found')

def logouthandle(request):
    logout(request)
    messages.success(request, "You've logged out")
    return redirect('home')

def changepassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated')
            return redirect('home')
        else:
            messages.error(request, 'Please Enter correct details')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'home/changepassword.html', {'form': form})
