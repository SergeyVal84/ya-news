from http import HTTPStatus
import pytest
from django.urls import reverse

@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, method',
    [('news:home', 'get'), ('users:login', 'get'), ('users:logout', 'post'), ('users:signup', 'get')]
)
def test_pages_availability_for_anonymous_user(client, name, method):
    url = reverse(name)
    response = getattr(client, method)(url)
    assert response.status_code == HTTPStatus.OK

@pytest.mark.django_db
def test_news_availability_for_anonymous_user(client, news):
    url = reverse('news:detail', kwargs={'pk': news.pk})
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK