from django.urls import re_path
from news_review.api import dashboard, news

urlpatterns = [
    # dashboard urls
    re_path(r'^dashboard/news_list/$', dashboard.news_list.as_view(), name='dashboard_news_list'),
    re_path(r'^dashboard/news_detail/(?P<pk>\d+)/$', dashboard.news_detail.as_view(), name='dashboard_news_detail'),
    re_path(r'^dashboard/mass_publish_news/$', dashboard.massPublishNews.as_view(), name='dashboard_massPublishNews'),

    # news urls
    re_path(r'^news_list/$', news.newsList.as_view(), name='news_list'),
    re_path(r'^news_detail/(?P<pk>\d+)/$', news.news_detail.as_view(), name='news_detail'),
    re_path(r'^last_news/(?P<category_id>\d+)/$', news.last_news.as_view(), name='last_news'),
]