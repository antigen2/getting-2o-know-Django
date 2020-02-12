from django.contrib import admin
from .models import Post


# admin.site.register(Post)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Список отображаемых полей
    list_display = ('title', 'slug', 'author', 'publish', 'status')
