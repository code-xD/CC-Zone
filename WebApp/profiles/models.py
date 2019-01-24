from blog.models import Post, Like
from django.contrib.auth.models import User
from django.db import models
# Create your models here.
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    post_counter = models.PositiveIntegerField(default=0)
    likes_counter = models.PositiveIntegerField(default=0)

    def update(self):
        self.likes_counter = Like.objects.all().filter(post__author=self.user).count()
        self.post_counter = Post.objects.all().filter(author=self.user).count()

    def __str__(self):
        return f'{self.user.first_name} Profile'

    def save(self):

        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)