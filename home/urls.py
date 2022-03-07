from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    path('add-blog/', add_blog, name='add_blog'),
    path('see-blog/', see_blog, name='see_blog'),
    path('blog-detail/<slug>', BlogPostDetailView.as_view(), name='blog_detail'),
    path('blog-delete/<id>', blog_delete, name='blog_delete'),
    path('blog-update/<slug>', blog_update, name='blog_update'),
    path('blogpost-like/<slug>', BlogPostLike, name="blogpost_like"),

]
