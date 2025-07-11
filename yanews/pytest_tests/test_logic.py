from pytest_django.asserts import assertRedirects
import pytest
from django.urls import reverse
from news.forms import BAD_WORDS, WARNING
from news.models import Comment, News


def test_user_can_create_comment(author_client, author, form_data, news):
    url = reverse('news:detail', kwargs={'pk': news.pk})
    response = author_client.post(url, data=form_data)
    assertRedirects(response, reverse('news:detail', kwargs={'pk': news.pk}) +'#comments')
    assert Comment.objects.count() == 1
    new_comment = Comment.objects.get()
    assert new_comment.news == news
    assert new_comment.author == author
    assert new_comment.text == form_data['text']

@pytest.mark.django_db
def test_anonymous_can_not_create_comment(client, form_data, news):
    url = reverse('news:detail', kwargs={'pk': news.pk})
    response = client.post(url, data=form_data)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 0

def test_user_cant_use_bad_words(author_client, form_data, news):
    url = reverse('news:detail', kwargs={'pk': news.pk})
    form_data['text'] = f'Какой-то текст, {BAD_WORDS[0]}'
    response = author_client.post(url, data=form_data)
    form = response.context['form']
    assert Comment.objects.count() == 0
    assert form.errors