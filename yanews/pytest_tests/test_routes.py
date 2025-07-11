from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects
from pytest_lazy_fixtures import lf

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
def test_pages_availability_for_anonymous_user(
    client, news, name, method, kwargs
):
    if kwargs is None:
        url = reverse(name)
    else:
        kwargs['pk'] = news.pk
        url = reverse(name, kwargs=kwargs)
    response = getattr(client, method)(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    [
        (lf('not_author_client'), HTTPStatus.NOT_FOUND),
        (lf('author_client'), HTTPStatus.OK)
    ],
)
@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete'),
)
def test_author_can_delete_edit_only_his_comments(
    parametrized_client, name, comments, expected_status
):
    url = reverse(name, args=(comments.id,))
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete'),
)
def test_anonimus_cant_edit_delete(client, name, comments):
    login_url = reverse('users:login')
    url = reverse(name, args=(comments.id,))
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
