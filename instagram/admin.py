from django.contrib import admin
from .models import Post, Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'photo', 'caption', 'location']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass