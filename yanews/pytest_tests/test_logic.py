from pytest_django.asserts import assertRedirects
import pytest
from django.urls import reverse
from news.forms import BAD_WORDS, WARNING
from news.models import Comment, News
from pytest_lazy_fixtures import lf
from http import HTTPStatus


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

def test_author_can_edit_only_his_comments(author_client, news, comments, form_data):
    url = reverse('news:detail', kwargs={'pk': news.pk})
    response = author_client.post(url, form_data)
    assertRedirects(response, reverse('news:detail', kwargs={'pk': news.pk}) +'#comments')
    comments.refresh_from_db()
    assert comments.text != form_data['text']

def test_author_can_edit_only_his_comments(not_author_client, news, comments, form_data):
    url = reverse('news:detail', kwargs={'pk': news.pk})
    response = not_author_client.post(url, form_data)
    assert response.status_code == HTTPStatus.FOUND
    comments_from_db = Comment.objects.get(id=news.id)
    assert comments.text == comments_from_db.text

def test_author_can_delete_comments(author_client, news, comments):
    url = reverse('news:delete', kwargs={'pk': news.pk})
    response = author_client.post(url)
    assertRedirects(response, reverse('news:detail', kwargs={'pk': comments.news.pk}) + '#comments')
    assert Comment.objects.count() == 0


def test_other_user_cant_delete_comments(not_author_client, news, comments):
    url = reverse('news:delete', kwargs={'pk': news.pk})
    response = not_author_client.post(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1
    