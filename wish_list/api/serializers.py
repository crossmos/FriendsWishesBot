from rest_framework import serializers

from .models import Wish, TelegramUser


class WishSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        slug_field='telegram_id',
        queryset=TelegramUser.objects.all()
    )

    class Meta:
        model = Wish
        fields = ('id', 'title', 'description', 'link', 'price', 'owner')


class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ('username', 'telegram_id')
