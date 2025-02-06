from django.http import JsonResponse, HttpResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_GET
from .models import News
import json

@require_GET
def last_news(request, category_id: int):
    """Получить последние 10 новостей"""
    if request.method == 'GET':
        limit = 10
        news = News.objects.filter(isDeleted=False, publish=True).order_by('-created')[:limit]
        if category_id:
            news = news.filter(category_id__pk=category_id)
        news_json = json.dumps(list(news.values()))
        return HttpResponse(news_json, content_type="application/json")

@require_GET
def news_detail(request, pk: int):
    """Получить новость по id"""
    if request.method == 'GET':
        try:
            news = News.objects.get(pk=pk, isDeleted=False, publish=True)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'News not found'}, status=400)
        news_json = json.dumps(list(news.values()))
        return HttpResponse(news_json, content_type="application/json")
    return HttpResponse(status=405)





@require_GET
def newsList(request):
    """Получить список новостей"""
    if request.method == 'GET':
        news = News.objects.filter(isDeleted=False, publish=True).order_by('-created')
        category_id = request.GET.get('category_id')
        if category_id:
            news = news.filter(category_id__pk=category_id)
        news_json = json.dumps(list(news.values()))
        return HttpResponse(news_json, content_type="application/json")
    return HttpResponse(status=405)
