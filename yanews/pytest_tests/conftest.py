import pytest
from django.conf import settings
from datetime import datetime, timedelta
from django.utils import timezone
# Импортируем класс клиента.
from django.test.client import Client

# Импортируем модель заметки, чтобы создать экземпляр.
from news.models import News, Comment

@pytest.fixture
def anonymous_client():
    return Client()

@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')

@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')

@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client

@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client

@pytest.fixture
def news(client):
    news_object = News.objects.create(
        title='Заголовок',
        text='Текст',
    )
    return news_object

@pytest.fixture
def comments(client, author, news):
    comment_object = Comment.objects.create(
        news=news,
        author=author,
        text='Текст',
    )
    return comment_object

@pytest.fixture
def news_list(client):
    today = timezone.now()
    news_list_object = [News(title=f'Заголовок {index}', text='Текст', date=today - timedelta(days=index)) for index in range(settings.NEWS_COUNT_ON_HOME_PAGE*10)]
    News.objects.bulk_create(news_list_object)
    return news_list_object

@pytest.fixture
def comments_list(news, author):
    now = timezone.now()
    for index in range(10):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Tекст {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()

@pytest.fixture
def form_data(news, author):
    return {'news': news, 'author': author, 'text': 'Новый текст',}