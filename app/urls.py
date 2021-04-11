from rest_framework import routers
from .api import UserViewSet, BookViewSet, BookFullTextViewSet, SubscriptionUserViewSet

router = routers.DefaultRouter()

router.register('api/user', UserViewSet, 'user')
router.register('api/book', BookViewSet, 'book')
router.register('api/book_full_text', BookFullTextViewSet, 'book_full_text')
router.register('api/subscription_user', SubscriptionUserViewSet, 'subscription_user')

urlpatterns = router.urls