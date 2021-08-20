from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db.models.fields.related import ForeignKey

# Create your models here.
#Model for post
class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=40)
    views = models.IntegerField(default=0)
    slug = models.CharField(max_length=140)
    timeStamp = models.DateTimeField(blank=True)

    def __str__(self):
        return self.title + ' by ' + self.author

class BlogComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timeStamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:13] + ".. By: " + self.user.username
