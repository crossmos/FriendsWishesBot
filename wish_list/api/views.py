from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from .models import TelegramUser, Wish
from .filters import WishFilter
from .serializers import TelegramUserSerializer, WishSerializer


class WishViewSet(viewsets.ModelViewSet):
    queryset = Wish.objects.all()
    serializer_class = WishSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = WishFilter
    http_method_names = ['get', 'post', 'patch', 'delete']


class TelegramUsers(viewsets.ModelViewSet):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer
    http_method_names = ['get', 'post']
    lookup_field = 'telegram_id'
