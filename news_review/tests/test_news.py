import json

import pytest
from django.test import Client
from django.urls import reverse

from news_review.models import User, Category, News


def get_client(user=None):
    client = Client()
    if user:
        client.force_login(user)
    return client


@pytest.mark.django_db(transaction=True)
class TestListNews:
    def test_list_news_filter_category(self):
        client = get_client()

        User.objects.create(name='Test Author', id=1, is_active=True)
        Category.objects.create(category_name='Test Category', id=1)
        Category.objects.create(category_name='Test Category 2', id=2)
        news = News.objects.create(news_name='Test News', news_text='This is test news text.', author_id_pk=1,
                                   category_id_pk=1, isDeleted=False)

        response = client.get(reverse('last_news', kwargs={'category_id': 1}))
        assert response.status_code == 200
        content = json.loads(response.content)
        assert len(content) == 1


@pytest.mark.django_db(transaction=True)
class TestNewsDetail:
    def test_can_see_not_deleted_and_published_news(self):
        Category.objects.create(category_name='Test Category', id=1)
        news = News.objects.create(news_name='Test News', news_text='This is test news text.', author_id_pk=1,
                                   category_id_pk=1, isDeleted=False, publish=True)

        client = get_client()
        response = client.get(reverse('news_detail', kwargs={'pk': news.id}))
        assert response.status_code == 200

    def test_cannot_see_deleted_news(self):
        Category.objects.create(category_name='Test Category', id=1)
        news = News.objects.create(news_name='Test News', news_text='This is test news text.', author_id_pk=1,
                                   category_id_pk=1, isDeleted=True, publish=True)

        client = get_client()
        response = client.get(reverse('news_detail', kwargs={'pk': news.id}))
        assert response.status_code == 404

    def test_cannot_see_unpublished_news(self):
        Category.objects.create(category_name='Test Category', id=1)
        news = News.objects.create(news_name='Test News', news_text='This is test news text.', author_id_pk=1,
                                   category_id_pk=1, isDeleted=False, publish=False)

        client = get_client()
        response = client.get(reverse('news_detail', kwargs={'pk': news.id}))
        assert response.status_code == 404
        news.refresh_from_db()
        assert news.publish == False

    def test_cannot_see_deleted_and_unpublished_news(self):
        Category.objects.create(category_name='Test Category', id=1)
        news = News.objects.create(news_name='Test News', news_text='This is test news text.', author_id_pk=1,
                                   category_id_pk=1, isDeleted=True, publish=False)

        client = get_client()
        response = client.get(reverse('news_detail', kwargs={'pk': news.id}))
        assert response.status_code == 404
