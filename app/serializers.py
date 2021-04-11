from rest_framework import serializers
from .models import User, Book, BookFullText, SubscriptionUser
from rest_framework.response import Response


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username', 'email', 'is_active')


class BookSerializer(serializers.ModelSerializer):
	class Meta:
		model = Book
		fields = ('title', 'image', 'decription')


class BookFullTextSerializer(serializers.ModelSerializer):
	class Meta:
		model = BookFullText
		fields = ('text', )


class SubscriptionUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = SubscriptionUser
		fields = ('user', 'date_end')
