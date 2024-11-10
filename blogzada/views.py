from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from .forms import UserForm, PostForm, EditPostForm
from .models import User, Post, Like, Dislike, Comment, Bookmark
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def index(request):
    return render(request, 'index.html')

def save_data(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        User.objects.create(name=name, email=email, password=password)
        messages.success(request, "Data saved successfully.")
        return redirect('index')
    return render(request, 'index.html')

def register_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User registered successfully.")
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')

@login_required
def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('index')

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Post created successfully.")
            return redirect('view_posts')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

@login_required
def view_posts(request):
    posts = Post.objects.all()
    return render(request, 'view_posts.html', {'posts': posts})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = EditPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully.")
            return redirect('view_posts')
    else:
        form = EditPostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    messages.success(request, "Post deleted successfully.")
    return redirect('view_posts')

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    like, created = Like.objects.get_or_create(post=post, user=user)
    if not created:
        like.delete()
        messages.success(request, "Like removed.")
    else:
        messages.success(request, "Post liked.")
    return redirect('view_posts')

@login_required
def dislike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    dislike, created = Dislike.objects.get_or_create(post=post, user=user)
    if not created:
        dislike.delete()
        messages.success(request, "Dislike removed.")
    else:
        messages.success(request, "Post disliked.")
    return redirect('view_posts')

@login_required
def comment_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        Comment.objects.create(post=post, user=request.user, text=comment_text)
        messages.success(request, "Comment added.")
    return redirect('view_posts')

@login_required
def bookmark_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    bookmark, created = Bookmark.objects.get_or_create(post=post, user=user)
    if not created:
        bookmark.delete()
        messages.success(request, "Bookmark removed.")
    else:
        messages.success(request, "Post bookmarked.")
    return redirect('view_posts')

# Funções de perfil e visualização de likes, dislikes, etc.
@login_required
def view_user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'view_user_profile.html', {'user': user})

@login_required
def edit_user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('view_user_profile', user_id=user_id)
    else:
        form = UserForm(instance=user)
    return render(request, 'edit_user_profile.html', {'form': form})

@login_required
def change_password(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        password = request.POST.get('password')
        user.set_password(password)
        user.save()
        messages.success(request, "Password changed successfully.")
        return redirect('view_user_profile', user_id=user_id)
    return render(request, 'change_password.html')
