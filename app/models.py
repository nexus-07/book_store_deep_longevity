import datetime
from collections import namedtuple

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
	def save(self, *args, **kwargs):
		new = self.pk is None
		super().save()

		if new:
			SubscriptionUser.subscribe(self, SubscriptionUser.REG_PERIOD)


class Book(models.Model):
	class TypeBook(models.IntegerChoices):
		"""Форма хранения и распостранения книг может быть разная"""
		full = 0  # полная книга одним файлом BooksFullText
		chapters = 1  # книга по главам BooksChapters

	title = models.CharField('Заголовок', max_length=256)
	created = models.DateTimeField('Дата и время добавления', auto_now_add=True)
	type_book = models.SmallIntegerField('Тип книги', choices=TypeBook.choices, default=0)
	image = models.CharField('Обложка', max_length=256, blank=True)
	description = models.CharField('Описание', max_length=500, blank=True)

	def __str__(self):
		return self.title


class BookFullText(models.Model):
	"""Полный текст книги."""
	book = models.OneToOneField(Book, verbose_name='Книга', related_name='book_full_text', on_delete=models.CASCADE)
	text = models.TextField('Текст книги')
	created = models.DateTimeField('Дата и время добавления', auto_now_add=True)
	# todo в методе save или на странице редактирвоания текста, надо отслеживать изменение текста и менять дату. Или отдельная модель изменения текста
	update = models.DateTimeField('Дата и время обновления', null=True)


class BookChapter(models.Model):
	"""Книга имеет множества глав."""
	book = models.ForeignKey(Book, verbose_name='Книга', related_name='book_charter', db_index=False, on_delete=models.CASCADE)
	title = models.CharField('Заголовок главы', max_length=256)
	number = models.SmallIntegerField('Номер главый')
	text = models.TextField('Текст главы')
	created = models.DateTimeField('Дата и время добавления', auto_now_add=True)
	# todo в методе save или на странице редактирвоания текста, надо отслеживать изменение текста главы и менять дату. Или отдельная модель изменения текста
	update = models.DateTimeField('Дата и время обновления', null=True)
	free_distribution = models.BooleanField('Бесплатное распространение', default=False)

	class Meta:
		unique_together = (('book', 'number'),)


class SubscriptionUser(models.Model):
	"""Подписка пользователя книги."""
	Period = namedtuple('Period', ['type_subscription', 'timedelta'])

	REG_PERIOD = Period(0, datetime.timedelta(days=14))
	MONTH_PERIOD = Period(1, datetime.timedelta(days=30))
	YEAR_PERIOD = Period(2, datetime.timedelta(days=365))

	period_by_name = {
		'month': MONTH_PERIOD,
		'year': YEAR_PERIOD,
	}

	user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Пользователь', related_name='subscription_user', on_delete=models.CASCADE)
	date_end = models.DateTimeField('Дата и время окончания действия подписки')

	@classmethod
	def subscribe(cls, user, period):
		# подписать пользователя на определенный период времени

		def get_period_obj(period):
			if isinstance(period, cls.Period):
				return period
			else:
				return cls.period_by_name[period]

		period = get_period_obj(period)

		subscribe_user = cls.objects.filter(user=user).first()
		if subscribe_user:
			subscribe_user.date_end = subscribe_user.date_end + period.timedelta
		else:
			subscribe_user = cls(user=user, date_end=timezone.now() + period.timedelta)

		subscribe_user.save()

		# добавить в историю тип подписки
		SubscriptionUserHistory.objects.create(user=user, type_subscription=period.type_subscription)


class SubscriptionUserHistory(models.Model):
	"""Исторрия одписки пользователей на книги."""
	class TypeSubscription(models.IntegerChoices):
		"""Тип подписки"""
		start = SubscriptionUser.REG_PERIOD.type_subscription, 'Регистрация'  # при регистрации на 2 недели
		mount = SubscriptionUser.MONTH_PERIOD.type_subscription, 'Месяц'  # на 1 месяц
		year = SubscriptionUser.YEAR_PERIOD.type_subscription, 'Год'  # на 1 год

	user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Пользователь', related_name='subscription_user_history', on_delete=models.CASCADE)
	type_subscription = models.SmallIntegerField('Тип подписки', choices=TypeSubscription.choices, default=0)
	created = models.DateTimeField('Дата и время создания', auto_now_add=True)

