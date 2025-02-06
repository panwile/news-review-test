import hashlib
import os
import random
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.http import JsonResponse, HttpResponse, Http404
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from .models import News
import json


@login_required
def news_list(request):
    """Получить список новостей, обновить новости"""
    if request.method == 'GET':
        news = News.objects.filter(isDeleted=False)
        if not request.user.is_staff:
            news = news.filter(author_id=request.user)
        news_json = serializers.serialize('json', news)
        return HttpResponse(news_json, content_type="application/json")

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            # TODO: complete
            default_image = open(os.path.join(settings.STATIC_ROOT, 'images', 'default_image.jpg'), 'rb')

            createdNews = News(news_name=data['news_name'], news_text=data['news_text'], author_id=data['author_id'], category_id=data['category_id'], image=ContentFile(default_image.read(), name=generate()))
            createdNews.save()
            return JsonResponse({'id': new_news.id}, status=200)
        except (ValueError, KeyError):
            return HttpResponse(status=400)

    return HttpResponse(status=405)

@login_required
def news_detail(request, pk: int):
    """Получить новость по id, обновить новость, удалить новость"""
    try:
        newsObject = News.objects.get(pk=pk, isDeleted=False)
        if not request.user.is_staff \
                and newsObject.author_id != request.user:
            return HttpResponse(status=403)
    except ObjectDoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET' and not news.isDeleted:
        news_json = serializers.serialize('json', [news, ])
        return HttpResponse(news_json, content_type="application/json")

    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            if not data.get('isDeleted'):
                news.news_name = data.get('news_name', news.news_name)
                news.news_text = data.get('news_text', news.news_text)
                news.publish = data.get('publish', news.publish)
                # TODO
                # news.author_id = data.get('author_id', news.author_id)
                # news.category_id = data.get('category_id', news.category_id)
                news.save()
            else:
                news.set_delete()
            return HttpResponse(status=200)
        except ValueError:
            return HttpResponse(status=400)
    # TODO
    # elif request.method == 'PATCH':
    #     try:
    #         data = json.loads(request.body)
    #         news.publish = data.get('publish', news.publish)
    #         news.save()
    #         return HttpResponse(status=200)
    #     except ValueError:
    #         return HttpResponse(status=400)

    return HttpResponse(status=405)

@login_required
def massPublishNews(request):
    """Batch публикация новостей"""
    if not request.user.is_staff:
        return HttpResponse(status=403)

    if request.method == 'PATCH':
        ok_news = []
        try:
            data = json.loads(request.body)
            news_ids = data['ids_for_publishing']
            for news_id in news_ids:
                try:
                    newsItem = (
                        News.objects.get(id=news_id))
                    newsItem.set_publish(send_email=False)
                    newsItem.save()
                    ok_news.append(news_id)
                except News.DoesNotExist:
                    print(f"News with id {news_id} does not exist.")
            return JsonResponse({'status': 'success'}, status=200)
        except KeyError as e:
            return JsonResponse({'error': 'Invalid payload, ids_for_publishing key not found.'}, status=400)
        except Exception as e:
            print(e)
            pass
        News.send_publish_email(ok_news)
    return HttpResponse(status=405)


def generate() -> str:
    random_hash = hashlib.sha256(str(random.getrandbits(256)).encode('utf-8')).hexdigest()
    return random_hash + '.jpg'


