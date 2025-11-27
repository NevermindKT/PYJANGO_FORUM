from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import CategoryForm
from .models import Category

def index(request):
    categories = Category.objects.all()
    return render(request, 'categories/index.html', {'categories': categories})

@login_required(login_url='/accounts/register/')
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('categories_index')
    else:
        form = CategoryForm()

    return render(request, 'categories/create_category.html', {'form': form})