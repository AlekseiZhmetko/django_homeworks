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

    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True, read_only=True)

    class Meta:
        model = Stock
        fields = ['address', 'positions']

    # def create(self, validated_data):
    #     # достаем связанные данные для других таблиц
    #     positions = validated_data.pop('positions')
    #
    #     # создаем склад по его параметрам
    #     stock = super().create(validated_data)
    #     for position in positions:
    #         position['stock'] = stock
    #         StockProduct.objects.create(**position)
    #     return stock


    def update_or_create(self, instance, validated_data):

        positions = validated_data.pop('positions')

        stock = super().update_or_create(self, instance)
        for position in positions:
            product = position['product']
            price = position['price']
            quantity = position['quantity']
            StockProduct.objects.update_or_create(
                stock=instance,
                product=product,
                defaults={'price': price, 'quantity': quantity}
            )
        return stock
