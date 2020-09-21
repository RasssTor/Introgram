from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UpdateMainImage, AddPost, AddComment, SearchForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Comment, User, Profile
from django.views.generic import View
from datetime import datetime
from django.http import HttpResponse
import os
from django.utils import timezone
from django.views.generic import ListView
from django.core.paginator import Paginator


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created! You can log in!')
            return redirect('login')
    else:
        return render(request, 'users/register.html', {'form': UserRegisterForm})
    return render(request, 'users/register.html', {'form': UserRegisterForm})


class SearchView(LoginRequiredMixin, ListView):

    paginate_by = 1
    model = Post
    template_name = 'users/search.html'
    context_object_name = 'posts'

    def get_queryset(self):
        hash = self.request.GET['hash']
        posts = Post.objects.all()
        for post in posts:
            if hash in post.tags.names():
                posts = post.tags.similar_objects()
                posts.append(post)
                break
        return posts

    def get_context_data(self, **kwargs):
        hash = self.request.GET['hash']
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.all()
        context['hash'] = hash
        context['search_form'] = SearchForm(
            initial={'hash': hash}
        )
        context['comments'] = comments
        return context



@login_required
def profile(request):
    profile_id = request.user.profile.id
    posts = Post.objects.filter(profile_id__exact=profile_id)
    posts_sorted = posts.order_by('-pub_date')
    comments = Comment.objects.filter(post_id__in=posts)
    # likes = Like.objects.filter(likes = request.user)
    return render(request, 'users/profile.html', {'posts': posts_sorted,
                                                  'profile': request.user.profile,
                                                  'form': UpdateMainImage,
                                                  'comment_form': AddComment,
                                                  'comments': comments
                                                  })

def home(request):
    return render(request, 'inst/base.html')

@login_required
def edit(request):
    return render(request, 'users/edit_profile.html')

@login_required
def update(request):
    print('update')
    info = request.POST
    person = User.objects.get(id=request.user.id)
    if info['email'] is not '':
        person.email = info['email']
    if info['description'] is not '':
        person.profile.description = info['description']
    if info['website'] is not '':
        person.profile.website = info['website']
    if info['name'] is not '':
        person.profile.name = info['name']
    if info['surname'] is not '':
        person.profile.surname = info['surname']
    if info['age'] is 0:
        person.profile.age = info['age']
    person.save()
    return redirect('/profile')

@login_required
def avatar_update(request):
    if request.method == 'POST':
        # delete old avatar
        try:
            os.remove('././media/profile_main_image/' + str(request.user.id) + '.jpg')
        except FileNotFoundError:
            pass
        # create and save new avatar
        person = User.objects.get_by_natural_key(request.user.username)
        request.FILES['file'].name = str(request.user.id) + '.jpg'
        person.profile.main_image = request.FILES['file']
        person.save()
        print(request.user.profile.main_image)
    return redirect('/profile')

@login_required
def add_post(request):
    if request.method == "POST":
        form = AddPost(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.profile = request.user.profile
            post.pub_date = datetime.now(tz=timezone.utc)
            post.save()
            post.tags.add(str(form.cleaned_data['tags']))
            post.save()
            form.save_m2m()
            return redirect('/profile')
    else:
        form = AddPost()
        return render(request, 'users/add_post.html', {'form': form})


class CommentView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post = self.request.POST
        comment, created = Comment.objects.get_or_create(post = Post.objects.get(id= post['id']),
                                                         author=request.user,
                                                         text= post['text'])

        return HttpResponse('')


class LikeView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        post = Post.objects.get(id=request.POST['id'])
        user = Profile.objects.get(id=post.profile.id)
        post_likes = eval(user.like)
        users_like = eval(post.liked_by)
        post_likes.append(post.id)
        user.like = post_likes
        user.save()
        users_like.append(str(request.user))
        post.liked_by = users_like
        post.save()
        return HttpResponse('')

    def get(self, request, *args, **kwargs):
        post = Post.objects.get(id=request.GET['id'])
        user = Profile.objects.get(id=post.profile.id)
        post_likes = eval(user.like)
        users_like = eval(post.liked_by)
        users_like.remove(str(request.user))
        post_likes.remove(post.id)
        user.save()
        post.liked_by = users_like
        post.save()
        return HttpResponse('')



class NewsView(LoginRequiredMixin, ListView):

    paginate_by = 2
    model = Post
    template_name = 'users/news.html'
    context_object_name = 'posts'

    def get_queryset(self):
        posts = Post.objects.order_by('-pub_date')
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.all()
        context['comments'] = comments
        return context

@login_required
def other_profile(request, username):
    if request.user.username == username:
        return redirect('profile')
    else:
        user = User.objects.get(username=username)
        posts = Post.objects.filter(profile=user.profile)
        comments = Comment.objects.all()
        return render(request, 'users/other_profile.html', {'profile': request.user.profile,
                                                            'other_profile': user.profile,
                                                            'posts': posts,
                                                            'comments': comments})


