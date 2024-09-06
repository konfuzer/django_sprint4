from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now
from django.db.models import Count
from django.urls import reverse

from .models import Category, Comment, Post
from .forms import PostForm, CustomUserCreationForm, CommentForm


User = get_user_model()

NUM_POSTS_ON_INDEX = 10


def paginate_queryset(request, queryset, num_per_page=NUM_POSTS_ON_INDEX):
    paginator = Paginator(queryset, num_per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def custom_profile_view(request):
    return render(request, 'blog/profile.html', {'profile': request.user})


def get_published_posts():
    return Post.objects.filter(
        is_published=True,
        pub_date__lt=now(),
        category__is_published=True,
    ).select_related('author', 'category', 'location')


def index(request):
    posts = get_published_posts().annotate(
        comment_count=Count('comments')).order_by('-pub_date')
    page_obj = paginate_queryset(request, posts)

    context = {
        'page_obj': page_obj,
    }

    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author == request.user:
        comments = post.comments.order_by('created_at')
        form = CommentForm()

        context = {
            'post': post,
            'comments': comments,
            'form': form
        }
        return render(request, 'blog/detail.html', context)

    post = get_object_or_404(
        Post,
        id=post_id,
        is_published=True,
        category__is_published=True,
        pub_date__lt=now()
    )
    comments = post.comments.order_by('created_at')
    form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'form': form
    }

    return render(request, 'blog/detail.html', context)


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug, is_published=True)
    posts = get_published_posts().filter(category=category)
    page_obj = paginate_queryset(request, posts)

    context = {
        'category': category,
        'page_obj': page_obj,
    }

    return render(request, 'blog/category.html', context)


def registration(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
    }

    return render(request, 'registration/registration_form.html', context)


def profile(request, username):
    profile = get_object_or_404(User, username=username)

    if request.user == profile:
        posts = (
            Post.objects.filter(author=profile)
            .annotate(comment_count=Count('comments')).order_by('-pub_date',)
        )
    else:
        posts = (
            get_published_posts()
            .filter(author=profile)
            .annotate(comment_count=Count('comments')).order_by('-pub_date',)
        )

    page_obj = paginate_queryset(request, posts)

    context = {
        'profile': profile,
        'page_obj': page_obj,
        'user': request.user,
        'first_name': profile.first_name,
        'last_name': profile.last_name,
    }

    return render(request, 'blog/profile.html', context)


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:profile', username=request.user.username)
    else:
        form = PostForm()

    context = {
        'form': form,
    }

    return render(request, 'blog/create.html', context)


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.author:
        return redirect('blog:post_detail', post_id=post_id)

    form = PostForm(request.POST or None, instance=post)
    context = {
        'form': form
    }
    if form.is_valid():
        form.save()

    return render(request, 'blog/create.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('blog:profile', username=request.user.username)
    else:
        form = UserChangeForm(instance=request.user)

    context = {
        'form': form,
    }

    return render(request, 'registration/registration_form.html', context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id, is_published=True)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog:post_detail', post_id=post.pk)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'form': form,
    }

    return render(request, 'blog/comment.html', context)


@login_required
def edit_comment(request, post_id, comment_id):
    post = get_object_or_404(Post, pk=post_id, is_published=True)
    comment = get_object_or_404(Comment, pk=comment_id, author=request.user)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', post_id=post.pk)
    else:
        form = CommentForm(instance=comment)

    context = {
        'post': post,
        'comment': comment,
        'form': form,
    }

    return render(request, 'blog/comment.html', context)


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id, author=request.user)
    form = PostForm()
    if request.method == 'POST':
        post.delete()
        return redirect('blog:index')
    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'blog/create.html', context)


@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(
        Comment, id=comment_id, post_id=post_id, author=request.user)

    if request.method == 'POST':
        comment.delete()
        return redirect(reverse('blog:post_detail', args=[post_id]))

    post = get_object_or_404(Post, pk=post_id)

    context = {
        'post': post,
    }

    return render(request, 'blog/comment.html', context)


@login_required
def profile_redirect(request):
    return redirect(reverse('blog:profile', args=[request.user.username]))
