import django_filters

from .models import Wish


class WishFilter(django_filters.FilterSet):
    owner_id = django_filters.NumberFilter(
        field_name='owner__telegram_id'
    )
    owner_username = django_filters.CharFilter(
        field_name='owner__username'
    )

    class Meta:
        model = Wish
        fields = ('title', 'description', 'link', 'price', 'owner')
