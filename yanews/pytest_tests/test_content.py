from django.urls import reverse

import pytest
from pytest_lazy_fixtures import lf

from news.forms import CommentForm


@pytest.mark.django_db
def test_news_count_sorted(client, news_list):
    url = reverse('news:home')
    response = client.get(url)
    news_list = response.context['news_list']
    all_date = [news.date for news in news_list]
    sorted_date = sorted(all_date, reverse=True)
    assert len(news_list) <= 10
    assert sorted_date == all_date


@pytest.mark.django_db
def test_comments_sorted(client, comments_list, comments, news):
    url = reverse('news:detail', kwargs={'pk': news.pk})
    response = client.get(url)
    news_object = response.context['news']
    comments_list = news_object.comment_set.all()
    all_comments_date = [comments.created for comments in comments_list]
    sorted_comments_date = sorted(all_comments_date)
    assert sorted_comments_date == all_comments_date


@pytest.mark.django_db
@pytest.mark.parametrize(
    'parametrized_client, expected_form',
    [
        (lf('anonymous_client'), False),
        (lf('author_client'), True)
    ],
)
def test_add_comments_form(parametrized_client, news, expected_form):
    url = reverse('news:detail', kwargs={'pk': news.pk})
    response = parametrized_client.get(url)
    if expected_form:
        assert 'form' in response.context
        assert isinstance(response.context['form'], CommentForm)
    else:
        assert 'form' not in response.context
