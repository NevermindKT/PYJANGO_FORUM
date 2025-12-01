from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CategoryForm
from .models import Category

def index(request):
    categories = Category.objects.all()
    return render(request, 'categories/index.html', {'categories': categories})

@login_required(login_url='/accounts/login/')
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('categories_index')
    else:
        form = CategoryForm()

    return render(request, 'categories/create_category.html', {'form': form})

def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if not request.user.is_staff:
        return HttpResponse("Недостаточно прав")

    category.delete()
    return redirect('categories_index')

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = category.posts.all().select_related('author')

    return render(request, 'categories/category_detail.html', {
        'category': category,
        'posts': posts,
    })