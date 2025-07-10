from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_news_count(client, news_list):
    url = reverse('news:home')
    response = client.get(url)
    news_list = response.context['news_list']
    assert len(news_list) <= 10
