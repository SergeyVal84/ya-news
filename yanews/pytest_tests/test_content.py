from django.urls import reverse
import pytest


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
    sorted_comments_date = sorted(all_comments_date, reverse=True)
    assert sorted_comments_date == all_comments_date
