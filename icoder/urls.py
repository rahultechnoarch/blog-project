from django.contrib import admin
from django.urls import path, include

#change admin panel details
admin.site.site_header = "BlogPost Admin"
admin.site.site_title = "BlogPost Admin Panel"
admin.site.index_title = "Welcome to BlogPost Admin Panel"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('blog/', include('blog.urls')),
]
