from django.contrib import admin
from .models import Profile
from .models import Post, Comment, Game

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Game)