from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_news_count(client, news_list):
    url = reverse('news:home')
    response = client.get(url)
    news_list = response.context['news_list']
    all_date = [news.date for news in news_list]
    sorted_date = sorted(all_date, reverse=True)
    assert len(news_list) <= 10
    assert sorted_date == all_date
