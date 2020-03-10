from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail


def post_share(request, post_id):
    # Получение статьи по идентификатору
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # форма была отправлена на сохранение
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Все поля формы прошли валидацию
            cd = form.cleaned_data
            # отправка электронной почты

            # абсолютная ссылка с содержанием http-сжемы и имени хоста
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) рекомендация к прочтению "{}}"'.format(
                cd['name'], cd['email'], post.title)
            message = 'Прочти "{}" в {}\n\n{}\'s коментарии: {}'.format(
                post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html',
                  {'post': post, 'form': form, 'sent': sent})


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
