from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from django.contrib import messages
from .forms import PostCreationForm, CommentForm
# Create your views here.


def home(request):
    post_dict = Post.objects.all().order_by('-date')
    for post in post_dict:
        short_view = post.content[:100]
        post.content = short_view
    context = {'posts': post_dict}
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


def detail(request, pk):
    comment_post = get_object_or_404(Post, id=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        print(form)
        if form.is_valid():
            comment_data = Comment(
                comment=form.cleaned_data['comment'],
                author=request.user,
                post=comment_post
            )
            comment_data.save()
            messages.success(request, 'Comment Submitted.')
            comments = Comment.objects.all().filter(post=comment_post).order_by('-date')
            return render(
                request,
                'blog/detail.html',
                {
                    'post': comment_post,
                    'form': CommentForm(),
                    'comments': comments
                }
            )
    else:
        form = CommentForm()
        comments = Comment.objects.all().filter(
            post=comment_post).order_by('-date'
                                        )
        return render(
            request, 'blog/detail.html',
            {
                'post': comment_post,
                'form': form,
                'comments': comments
            }
        )
