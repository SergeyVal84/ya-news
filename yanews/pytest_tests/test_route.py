from http import HTTPStatus
import pytest
from django.urls import reverse

@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, method',
    [('news:home', 'get'), ('users:login', 'get'), ('users:logout', 'post'), ('users:signup', 'get')]
)
def test_pages_availability_for_anonymous_user(client, name, method):
    # ваш тест здесь

    url = reverse(name)  # Получаем ссылку на нужный адрес.
    response = getattr(client, method)(url)  # Выполняем запрос.
    assert response.status_code == HTTPStatus.OK