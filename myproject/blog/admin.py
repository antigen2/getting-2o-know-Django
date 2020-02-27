from django.contrib import admin
from .models import Post


# admin.site.register(Post)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Список отображаемых полей
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    # Блок фильтрации списка по перечисленным полям (справа)
    list_filter = ('status', 'created', 'publish', 'author')
    # Строка поиска
    search_fields = ('title', 'body')
    # автоматическое заполнение, генерирует из поля title
    # (при создании новой статьи)
    prepopulated_fields = {'slug': ('title', )}
    # поле author содержит поле поиска
    raw_id_fields = ('author', )
    # навигация по датам (под полем поиска)
    date_hierarchy = 'publish'
    # сортировка по умолчанию по полям
    ordering = ('status', 'publish')
