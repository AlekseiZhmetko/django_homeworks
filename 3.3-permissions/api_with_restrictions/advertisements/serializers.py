from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement, AdvertisementStatusChoices
from rest_framework.exceptions import ValidationError
from pprint import pprint


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        # TODO: добавьте требуемую валидацию
        user_id = self.context.get("request").user.id
        # print(user_id)
        status = data.get('status')
        if status is None or status == 'OPEN':
            creator_open_adv = Advertisement.objects.filter(creator_id=user_id, status='OPEN').values().count()
            if creator_open_adv >= 10:
                raise ValidationError('У пользователя может быть не больше 10 открытых объявлений.')
            else:
                print('Объявление успешно добавлено')
                return data
        else:
            return data
