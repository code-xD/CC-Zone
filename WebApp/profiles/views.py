from django.shortcuts import render, redirect
from .models import Profile, Post, Like
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserCreationForm, ProfileCreationForm
from PIL import Image


def home(request, username):
    for profile in Profile.objects.all().filter(user__username=username):
        profile.update()
        profile.save()
    req_prof = Profile.objects.all().filter(user__username=username)
    print(req_prof)
    context = {'profiles': req_prof}
    return render(request, 'profiles/home.html', context)


@login_required
def create(request):
    try:
        prof = request.user.profile
        if request.method == 'POST':
            u_form = UserCreationForm(request.POST, instance=request.user)
            p_form = ProfileCreationForm(request.POST, request.FILES, instance=request.user.profile)
            if u_form.is_valid() and p_form.is_valid():
                usr_profile_img = p_form.cleaned_data['image']
                u_form.save()
                prof = Profile.objects.get(user=request.user)
                prof.image = usr_profile_img
                prof.save()
                img_save(prof, request)
                prof.save()
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
    except:
        if request.method == 'POST':
            u_form = UserCreationForm(request.POST, instance=request.user)
            p_form = ProfileCreationForm(request.POST, request.FILES)
            if u_form.is_valid() and p_form.is_valid():
                usr_profile_img = p_form.cleaned_data['image']
                u_form.save()
                prof = Profile(user=request.user, image=usr_profile_img)
                prof.save()
                img_save(prof, request)
                prof.save()
                messages.success(request, f'Your account has been updated.')
                return redirect('blog-home')
        else:
            u_form = UserCreationForm(instance=request.user)
            p_form = ProfileCreationForm()
            context = {
                'u_form': u_form,
                'p_form': p_form
            }
            return render(request, 'profiles/create.html', context)


def img_save(prof, request):
    img = Image.open(prof.image.path)
    if img.height != 300 or img.width != 300:
        output_size = (300, 300)
        img.thumbnail(output_size)
        img.save(prof.image.path)


def no_of_likes(post):
    occurances = Like.objects.all().filter(post=post).count()
    return occurances


@login_required
def base_create(request):
    try:
        prof = request.user.profile
        return redirect('/')
    except:
        if request.method == 'POST':
            u_form = UserCreationForm(request.POST, instance=request.user)
            p_form = ProfileCreationForm(request.POST, request.FILES)
            if u_form.is_valid() and p_form.is_valid():
                usr_profile_img = p_form.cleaned_data['image']
                u_form.save()
                prof = Profile(user=request.user, image=usr_profile_img)
                prof.save()
                img_save(prof, request)
                prof.save()
                messages.success(request, f'Your account has been updated.')
                return redirect('blog-home')
        else:
            u_form = UserCreationForm(instance=request.user)
            p_form = ProfileCreationForm()
            context = {
                'u_form': u_form,
                'p_form': p_form
            }
            return render(request, 'profiles/create.html', context)


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
