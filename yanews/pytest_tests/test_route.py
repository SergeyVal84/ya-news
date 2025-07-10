from http import HTTPStatus
import pytest
from django.urls import reverse

@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, method, kwargs',
    [
        ('news:home', 'get', None),
        ('users:login', 'get', None),
        ('users:logout', 'post', None),
        ('users:signup', 'get', None),
        ('news:detail', 'get', {'pk': None})
    ]
)
def test_pages_availability_for_anonymous_user(client, news, name, method, kwargs):
    if kwargs is None:
        url = reverse(name)
    else:
        kwargs['pk'] = news.pk
        url = reverse(name, kwargs=kwargs)
    response = getattr(client, method)(url)
    assert response.status_code == HTTPStatus.OK

@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete'),
)
def test_author_can_delete_edit_comments(author_client, name, comments):
    url = reverse(name, args=(comments.id,))
    response = author_client.get(url)
    assert response.status_code == HTTPStatus.OK 


