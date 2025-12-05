from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm
from categories.models import Category
from .models import Post, Comment


@login_required
def create_post(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.category = category
            post.author = request.user
            post.save()
            return redirect('category_detail', category_id)
    else:
        form = PostForm()

    return render(request, 'posts/create_post.html', {
        'form': form,
        'category': category
    })

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user != post.author and not request.user.is_staff:
        return HttpResponse("Недостаточно прав.")

    category_id = post.category.id
    post.delete()
    return redirect('category_detail', category_id)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all().order_by('-created_at')

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('/accounts/login/')

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk)
    else:
        form = CommentForm()

    return render(request, 'posts/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.author != request.user and not request.user.is_staff:
        return HttpResponse("Недостаточно прав")

    post_id = comment.post.id
    comment.delete()
    return redirect('post_detail', pk=post_id)