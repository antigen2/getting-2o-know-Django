from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView


# аналог ф-ии post_list(request)
class PostListView(ListView):
    # переопрелелили запрос, только опубликованные
    queryset = Post.published.all()
    # posts - переменная контекста HTML шаблона,
    # в кот. будет храниться список объектов (object_list по умолчанию)
    context_object_name = 'posts'
    # отображать по 3 объекта на страницу
    paginate_by = 3
    # шаблон для формирования страницы
    template_name = 'blog/post/list.html'


# Обработчик постов. request - объект запроса
def post_list(request):
    # # Если отображение без страниц, все на одной
    # # posts = Post.published.all()
    # # return render(request, 'blog/post/list.html', {'posts': posts})
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)   # 3 статьи на стр
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Если страница НЕ ЦЕЛОЕ число, возвращаем 1-ую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # Если номер стр больше, чем общее кол-во, возвращаем последнюю стр
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})


# Обработчик страницы статьи
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published',
                             publish__year=year, publish__month=month,
                             publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})


#
