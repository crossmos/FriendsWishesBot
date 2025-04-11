from django.db import models


class TelegramUser(models.Model):
    username = models.CharField(max_length=128)
    telegram_id = models.IntegerField(unique=True)


class Wish(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    link = models.TextField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    owner = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    create_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ('-create_at',)
