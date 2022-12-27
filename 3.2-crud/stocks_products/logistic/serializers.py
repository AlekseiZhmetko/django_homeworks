from rest_framework import serializers

from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    def destroy(self, instance):
        return instance.delete()


class ProductPositionSerializer(serializers.ModelSerializer):
    # настройте сериализатор для позиции продукта на складе
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['address', 'positions']

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = super().create(validated_data)
        for position in positions:
            position['stock'] = stock
            StockProduct.objects.create(**position)
        return stock

    def update_or_create(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update_or_create(instance, positions)
        for position in positions:
            position['stock'] = stock
            StockProduct.objects.update_or_create(defaults=instance, positions)
        return stock


# create_or_update() не работает - разобраться:
# AssertionError: The `.create()` method does not support writable nested fields by default.
# Write an explicit `.create()` method for serializer `logistic.serializers.StockSerializer`,
# or set `read_only=True` on nested serializer fields.