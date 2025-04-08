from rest_framework.routers import DefaultRouter

from django.urls import path, include

from .views import WishViewSet, TelegramUsers


v1_router = DefaultRouter()
v1_router.register('wishes', WishViewSet)
v1_router.register('telegram_users', TelegramUsers)

urlpatterns = [
    path('v1/', include(v1_router.urls))
]
