from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

from .models import User, Book, BookFullText, SubscriptionUser
from .serializers import UserSerializer, BookSerializer, BookFullTextSerializer, SubscriptionUserSerializer
from django.shortcuts import get_object_or_404
from django.utils import timezone

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer


class BookViewSet(viewsets.ModelViewSet):
	queryset = Book.objects.all()
	serializer_class = BookSerializer


class BookFullTextViewSet(viewsets.ModelViewSet):
	queryset = BookFullText.objects.all()
	serializer_class = BookFullTextSerializer

	def retrieve(self, request, pk=None):
		# получение текста книги только для подписчиков
		book_full_text = get_object_or_404(self.queryset, book=pk)

		if SubscriptionUser.objects.filter(user=request.user, date_end__gt=timezone.now()).exists():
			serializer = self.serializer_class(book_full_text)

			return Response(serializer.data)
		else:
			content = {
				'status': 'request was permitted'
			}

			return Response(content)


class SubscriptionUserViewSet(viewsets.ModelViewSet):
	queryset = SubscriptionUser.objects.all()
	serializer_class = SubscriptionUserSerializer
	authentication_classes = (TokenAuthentication,)

	def create(self, request):
		# активируем подписку для пользователя
		# {'user_id': '', status: 'ok', 'period': 'month/year'}, либо {'user_id': '', status: 'error', 'msg': ''})
		msg = request.POST.get('msg', '')

		if request.POST['status'] == 'ok':
			user = User.objects.filter(pk=request.POST['user_id']).first()

			if user:
				SubscriptionUser.subscribe(user, request.POST['period'])

				return Response({'status': 'ok'})

			msg = 'Пользователеь не найден'

		content = {
			'msg': msg,
			'status': 'error',
		}

		return Response(content)
