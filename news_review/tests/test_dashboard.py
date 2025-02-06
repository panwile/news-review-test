import json
import pytest
from django.urls import reverse
from django.test import Client

from news_review.models import User, Category, News


def get_client(user=None):
    client = Client()
    if user:
        client.force_login(user)
    return client


@pytest.mark.django_db(transaction=True)
class TestNewsList:
    def test_news_list_200(self):
        user = User.objects.create(name='Test Author', id=1, is_active=True)
        Category.objects.create(category_name='Test Category', id=1)

        client = get_client(user)
        # Проверка POST запроса.
        post_data = {
            'news_name': 'Test News',
            'news_text': 'This is test news text.',
            'author_id': 1,
            'category_id': 1,
        }
        response = client.post(reverse('dashboard_news_list'), data=json.dumps(post_data), content_type='application/json')
        assert response.status_code == 200
        assert 'id' in json.loads(response.content)

        # Проверка GET запроса.
        response = client.get(reverse('dashboard_news_list'))
        assert response.status_code == 200
        content = json.loads(response.content)
        assert len(content) == 1


@pytest.mark.django_db(transaction=True)
class TestMassPublishNews:
    def test_mass_publish_news_200(self):
        user = User.objects.create(name='Test Author', id=1, is_active=True, is_staff=True)
        client = get_client(user)
        Category.objects.create(category_name='Test Category', id=1)
        News.objects.create(news_name='Test News', news_text='This is test news text.', author_id_pk=1,
                            category_id_pk=1, isDeleted=False)

        response = client.patch(reverse('dashboard_massPublishNews'), data=json.dumps({'ids_for_publishing': [1]}),
                                content_type='application/json')
        assert response.status_code == 200
