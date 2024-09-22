from rest_framework import serializers
from .models import NetworkNode, Product


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product model."""
    class Meta:
        model = Product
        fields = ['id', 'name', 'model', 'release_date']

    def validate_name(self, value):
        """Validates that the name is not longer than 50 characters."""
        if len(value) > 50:
            raise serializers.ValidationError(
                "Name must not exceed 50 characters."
            )
        return value


class NetworkNodeSerializer(serializers.ModelSerializer):
    """Serializer for NetworkNode model, including related products."""
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = NetworkNode
        fields = [
            'id', 'name', 'email', 'country', 'city', 'street',
            'house_number', 'debt_to_supplier', 'supplier', 'products', 'created_at'
        ]
        read_only_fields = ['debt_to_supplier']

    def update(self, instance, validated_data):
        """Ensures 'debt_to_supplier' is not updated."""
        validated_data.pop('debt_to_supplier', None)
        return super().update(instance, validated_data)
