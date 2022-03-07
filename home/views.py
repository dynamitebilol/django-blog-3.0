from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView

from .form import *



def home(request):
    context = {'blogs': BlogModel.objects.all()}
    return render(request, 'home.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')


def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')


def BlogPostLike(request, slug):
    post = get_object_or_404(BlogModel, id=request.POST.get('blogpost_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect('blog_detail', slug=slug)


class BlogPostDetailView(DetailView):
    model = BlogModel
    template_name ='blog_detail.html'
    context_object_name = 'object'


    def get_context_data(self, **kwargs):

        data = super().get_context_data(**kwargs)

        comments_connected = BlogComment.objects.filter(
            blogpost_connected=self.get_object()).order_by('-date_posted')
        data['comments'] = comments_connected
        if self.request.user.is_authenticated:
            data['comment_form'] = NewCommentForm(instance=self.request.user)

        likes_connected = get_object_or_404(BlogModel, slug=self.kwargs['slug'])
        liked = False
        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True
        data['number_of_likes'] = likes_connected.number_of_likes()
        data['post_is_liked'] = liked

        return data


    def post(self, request, *args, **kwargs):
        new_comment = BlogComment(content=request.POST.get('content'),
                                      author=self.request.user,
                                      blogpost_connected=self.get_object())
        new_comment.save()
        return self.get(self, request, *args, **kwargs)


def blog(request, slug):
    context = {}
    try:
        blog_obj = BlogModel.objects.filter(slug=slug).first()
        context['blog_obj'] = blog_obj
    except Exception as e:
        print(e)
    return render(request, 'blog_detail.html', context)



def add_blog(request):
    context = {'form': BlogForm}
    try:
        if request.method == 'POST':
            form = BlogForm(request.POST)
            print(request.FILES)
            image = request.FILES['image']
            title = request.POST.get('title')
            user = request.user

            if form.is_valid():
                content = form.cleaned_data['content']

            blog_obj = BlogModel.objects.create(
                user=user, title=title,
                content=content, image=image
            )
            print(blog_obj)
            return redirect('/add-blog/')

    except Exception as e:
        print(e)
    return render(request, 'add_blog.html', context)

def see_blog(request):
    context = {}
    try:
        blog_objs = BlogModel.objects.filter(user=request.user)
        context['blog_objs'] = blog_objs
    except Exception as e:
        print(e)
    return render(request, 'see_blog.html', context)


def blog_update(request, slug):
    context = {}
    try:

        blog_obj = BlogModel.objects.get(slug=slug)

        if blog_obj.user != request.user:
            return redirect('/')
        initial_dict = {'content': blog_obj.content}
        form = BlogForm(initial=initial_dict)
        if request.method == 'POST':
            form = BlogForm(request.POST)
            print(request.FILES)
            image = request.FILES['image']
            title = request.POST.get('title')
            user = request.user

            if form.is_valid():
                content = form.cleaned_data['content']

            blog_obj = BlogModel.objects.create(
                user=user, title=title,
                content=content, image=image
            )
        context['blog_obj'] = blog_obj
        context['form'] = form
    except Exception as e:
        print(e)

    return render(request, 'update_blog.html', context)


def blog_delete(request, id):
    try:
        blog_obj = BlogModel.objects.get(id=id)

        if blog_obj.user == request.user:
            blog_obj.delete()
    except Exception as e:
        print(e)

    return redirect('/see-blog/')

