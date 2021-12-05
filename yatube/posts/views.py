from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from yatube.settings import ITEMS_PER_PAGE

from .forms import CommentForm, PostForm
from .models import Follow, Group, Post, User


def pagination(request, queryset):
    paginator = Paginator(queryset, ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return {
        'paginator': paginator,
        'page_namber': page_number,
        'page_obj': page_obj,
    }


def index(request):
    post_list = Post.objects.all()
    context = pagination(request, post_list)
    template = 'posts/index.html'
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    context = {
        'group': group,
        'posts': posts,
    }
    context.update(pagination(request, posts))
    template = 'posts/group_list.html'
    return render(request, template, context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.posts.all()
    count_user_posts = post_list.count()
    title = username
    following = request.user.is_authenticated and Follow.objects.filter(
        user=request.user, author=author).exists()
    context = {
        'author': author,
        'count_user_posts': count_user_posts,
        'title': title,
        'following': following,
    }
    context.update(pagination(request, post_list))
    template = 'posts/profile.html'
    return render(request, template, context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comment_form = CommentForm()
    comments = post.comments.all()
    count = post.author.posts.count()
    template = 'posts/post_detail.html'
    context = {
        'post': post,
        'count': count,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    template = 'posts/create_post.html'
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
    )
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        form.save()
        return redirect('posts:profile', post.author)
    return render(request, template, {'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author == request.user:
        form = PostForm(
            request.POST or None,
            files=request.FILES or None,
            instance=post
        )
        if form.is_valid():
            form.save()
            return redirect('posts:post_detail', post_id)

    template = 'posts/create_post.html'
    context = {
        'form': form,
        'is_edit': True,
    }
    return render(request, template, context)


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
    # информация о текущем пользователе доступна в переменной request.user
    following = Follow.objects.filter(user=request.user).all()
    author_list = []
    for author in following:
        author_list.append(author.author.id)
    post_list = Post.objects.filter(author__in=author_list).all()
    context = pagination(request, post_list)
    template = 'posts/follow.html'
    return render(request, template, context)


@login_required
def profile_follow(request, username):
    # подписаться на автора
    user = request.user
    author = get_object_or_404(User, username=username)
    check_follow = Follow.objects.filter(
        user=user.id, author=author.id).count()
    if check_follow == 0 and author.id != user.id:
        Follow.objects.create(user=request.user, author=author)
    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    # отписаться от автора
    user = request.user
    author = get_object_or_404(User, username=username)
    check_follow = Follow.objects.filter(
        user=user.id, author=author.id).count()
    if check_follow == 1:
        Follow.objects.filter().delete()
    return redirect('posts:profile', username=username)
