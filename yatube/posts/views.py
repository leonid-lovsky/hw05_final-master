from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.cache import cache_page

from .forms import PostForm, CommentForm
from .models import Group, Post, Follow

User = get_user_model()

ITEMS_PER_PAGE = 10
INDEX_CACHE_TIMEOUT = 20


def create_page_obj(request, items, items_per_page):
    page_number = request.GET.get('page')
    paginator = Paginator(items, items_per_page)
    return paginator.get_page(page_number)


@cache_page(INDEX_CACHE_TIMEOUT)
def index(request):
    posts = Post.objects.all()
    page_obj = create_page_obj(request, posts, ITEMS_PER_PAGE)
    context = {
        'page_obj': page_obj,
        'index': True,
    }
    return render(request, 'posts/index.html', context)


def group_list(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    page_obj = create_page_obj(request, posts, ITEMS_PER_PAGE)
    context = {
        'page_obj': page_obj,
        'group': group,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    page_obj = create_page_obj(request, posts, ITEMS_PER_PAGE)
    context = {
        'page_obj': page_obj,
        'author': author,
    }
    if request.user.is_authenticated:
        context['following'] = (
            Follow.objects.filter(user=request.user, author=author).exists()
        )
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    context = {
        'post': post,
        'form': CommentForm(),
        'comments': post.comments.all(),
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
    )

    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', username=request.user.username)

    context = {
        'form': form,
        'is_edit': False
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return redirect('posts:post_detail', post_id=post_id)

    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )

    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)

    context = {
        'post': post,
        'form': form,
        'is_edit': True
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    posts = Post.objects.filter(author__following__user=request.user).all()
    page_obj = create_page_obj(request, posts, ITEMS_PER_PAGE)
    context = {
        'page_obj': page_obj,
        'follow': True
    }
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if request.user != author:
        author.following.get_or_create(user=request.user)
    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    author.following.filter(user=request.user).delete()
    return redirect('posts:profile', username=username)
