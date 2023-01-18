from django_filters import rest_framework as filters

from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    # TODO: задайте требуемые фильтры
    created_at = filters.DateFromToRangeFilter()
    creator = filters.CharFilter(field_name='creator__id')
    status = filters.CharFilter(field_name='status')
    class Meta:
        model = Advertisement
        fields = ['created_at', 'creator', 'status']
