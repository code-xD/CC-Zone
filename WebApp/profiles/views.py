from django.shortcuts import render, redirect
from .models import Profile
from blog.models import Post, Like
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserCreationForm, ProfileCreationForm

def home(request, username):
    post_dict = Post.objects.all().filter(author__username=username).order_by('-date')[:5]
    for post in post_dict:
        short_view = post.content[:100]
        post.content = short_view
        post.likes = no_of_likes(post)

    for profile in Profile.objects.all().filter(user__username=username):
        profile.update()
        profile.save()

    req_prof = Profile.objects.all().filter(user__username=username)
    print(req_prof)
    context = {'profiles': req_prof, 'posts': post_dict}
    return render(request, 'profiles/home.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        u_form = UserCreationForm(request.POST, instance=request.user)
        p_form = ProfileCreationForm(request.POST, request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated.')
            return redirect('blog-home')
    else:
        u_form = UserCreationForm(instance=request.user)
        p_form = ProfileCreationForm(instance=request.user.profile)
        context = {
            'u_form': u_form,
            'p_form': p_form
        }
        return render(request, 'profiles/create.html', context)

def no_of_likes(post):
    occurances = Like.objects.all().filter(post=post).count()
    return occurances

@login_required
def my_post(request, pk):
    post_dict = []
    for post in Post.objects.all().order_by('-date'):
        if post.author == request.user:
            short_view = post.content[:100]
            post.content = short_view
            post.likes = no_of_likes(post)
            post_dict.append(post)
    context = {'posts': post_dict, 'act': True}
    return render(request, 'blog/home.html', context)
