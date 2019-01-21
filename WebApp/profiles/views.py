from django.shortcuts import render, redirect
from .models import Profile, Post, Like
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserCreationForm, ProfileCreationForm
from PIL import Image


def home(request, pk):
    for profile in Profile.objects.all().filter(pk=pk):
        profile.update()
        profile.save()
    context = {'profile': Profile.objects.all().filter(pk=pk)[0]}
    return render(request, 'profiles/home.html', context)


@login_required
def create(request):
    req_user = request.user
    try:
        user_check = req_user.profile
        return redirect('blog-home')
    except:
        if request.method == 'POST':
            u_form = UserCreationForm(request.POST)
            p_form = ProfileCreationForm(request.POST,
                                         request.FILES)
            if u_form.is_valid() and p_form.is_valid():
                usr_profile = p_form.save(commit=False)
                usr_info = u_form.save(commit=False)
                request.user.first_name = usr_info.first_name
                request.user.last_name = usr_info.last_name
                request.user.email = usr_info.email
                request.user.save()
                prof = Profile(user=request.user, image=usr_profile.image)
                prof.save()
                img = Image.open(prof.image.path)
                if img.height != 300 or img.width != 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(prof.image.path)
                prof.save()
                messages.success(request, f'Your account has been created.')
                return redirect('blog-home')

        else:
            u_form = UserCreationForm(instance=request.user)
            p_form = ProfileCreationForm()

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
