from django.shortcuts import render, redirect
from .models import Post
from django.contrib import messages
from .forms import PostCreationForm
# Create your views here.


def home(request):
    context = {'posts': Post.objects.all().order_by('-date')}
    return render(request, 'blog/home.html', context)


def compose(request):
    if request.method == 'POST':
        form = PostCreationForm(request.POST)
        if form.is_valid():
            post_data = form.save(commit=False)
            post_data.author = request.user
            post_data.save()
            messages.success(request, f'Blog Posted Successfully.')
            return redirect('blog-home')
    else:
        form = PostCreationForm()
        return render(request, 'blog/create.html', {'form': form})
