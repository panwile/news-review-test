from typing import List
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
# Create your models here.
class News(models.Model):
    news_name = models.CharField(max_length=255, verbose_name='Название новости')
    news_text = models.TextField(
        verbose_name='Текст новости',
    )
    image = models.ImageField()
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    publish = models.BooleanField(
        default=False, verbose_name='Опубликовано'
    )
    author_id = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='Автор')
    category_id = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    isDeleted = models.BooleanField(
        default=False, verbose_name='Удалено')

    def __str__(self):
        return self.news_name

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def set_publish(self, send_email=True):
        if self.publish:
            raise ValueError('Already published')
        self.publish = True
        self.save()

        if send_email:
            self.send_publish_email([self.id])


    @classmethod
    def send_publish_email(cls, news_ids: List[int]):
        send_mail(
            'Публикация новостей',
            'Были опубликованы новости с id: {}'.format(', '.join(map(str, news_ids))),
            ['admin@news-review.test'],
            fail_silently=False,
        )



    def set_delete(self):
        if self.isDeleted:
            raise ValueError('Already deleted')
        self.isDeleted = True
        self.save()

class Category(models.Model):
    category_name = models.CharField(max_length=255, verbose_name='Название категории')

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'




class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=128, blank=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False, verbose_name='Сотрудник')

    date = models.DateField(auto_now_add=True, blank=True)

    USERNAME_FIELD = 'email'
