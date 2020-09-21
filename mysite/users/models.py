from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    main_image = models.ImageField(default='default.jpg', upload_to='profile_main_image/')
    description = models.CharField(default='', max_length=200)
    website = models.CharField(default='', max_length=100)
    name = models.CharField(default='', max_length= 100)
    surname = models.CharField(default='', max_length=100)
    age = models.IntegerField(default=0)
    like = models.TextField(default='[]')

    def __str__(self):
        return f'{self.user.username}'


class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    liked_by = models.TextField(default='[]')
    image = models.ImageField(upload_to='media/profile_images')
    description = models.CharField(default='', max_length=100)
    tags = TaggableManager()
    pub_date = models.DateTimeField('Publication date')

    def __str__(self):
        return f'{self.profile} photo {self.id}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=50)

class Game(models.Model):
    gamers = models.TextField(default='[]')
    active_gamer = models.IntegerField(default=None)
    field = models.IntegerField(default=2)

