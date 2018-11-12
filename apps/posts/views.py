from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import PostForm, CommentForm
from .models import Post, Comment

def post_list(request):
    post_list = Post.objects.all()
    return render(request, 'posts/post_list.html', {'post_list': post_list})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect(post)
    else:
        form = PostForm()

    return render(request, 'posts/post_form.html', {
        'form':form
    })

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm()
    return render(request, 'posts/post_detail.html', {
        'post': post,
        'form': form,
    })

@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.user != request.user:
        return redirect('posts:list')

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect(post)
    else:
        form = PostForm(instance=post)

    return render(request, 'posts/post_form.html', {
        'form': form,
    })

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.user != request.user:
        return redirect('posts:list')

    if request.method == 'POST':
        post.delete()
        return redirect('posts:list')

    return render(request, 'posts/post_confirm_delete.html', {
        'post': post,
    })

@login_required
@require_POST
def comment_create(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post = post
        comment.save()

    return redirect('posts:detail', post_id)

@login_required
@require_POST
def comment_delete(request, post_id, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.user != request.user:
        return redirect('posts:list')

    comment.delete()
    return redirect('posts:detail', post_id)

