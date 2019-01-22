from django.shortcuts import render, redirect, get_object_or_404

from .models import Post, Comment, Like
from django.contrib import messages
from .forms import PostCreationForm, CommentForm

from django.contrib.auth.decorators import login_required
# Create your views here.


def no_of_likes(post):
    occurances = Like.objects.all().filter(post=post).count()
    return occurances


def home(request):
    post_dict = Post.objects.all().order_by('-date')
    for post in post_dict:
        short_view = post.content[:100]
        post.content = short_view
        post.likes = no_of_likes(post)
    context = {'posts': post_dict}
    return render(request, 'blog/home.html', context)


@login_required
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
    comment_post.likes = no_of_likes(comment_post)
    if request.method == 'POST' and "like" not in request.POST:
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

    elif request.method == 'POST' and "like" in request.POST:
        form = CommentForm()
        comments = Comment.objects.all().filter(
            post=comment_post).order_by('-date'
                                        )
        like_instance = Like(author=request.user, post=comment_post)
        for like_element in Like.objects.all().filter(post=comment_post):
            if str(like_element) == str(like_instance):
                Like.objects.filter(author=request.user, post=comment_post).delete()
                comment_post.likes = no_of_likes(comment_post)
                return render(
                    request, 'blog/detail.html',
                    {
                        'post': comment_post,
                        'form': form,
                        'comments': comments
                    }
                )

        like_instance.save()
        comment_post.likes = no_of_likes(comment_post)
        return render(
            request, 'blog/detail.html',
            {
                'post': comment_post,
                'form': form,
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
