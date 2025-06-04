from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from libreria.models import DetalleCompra, Libro, Compra



class DetalleCompraSerializer(serializers.ModelSerializer):
    libro_titulo = serializers.CharField(source='libro.titulo', read_only=True)
    compra_id = serializers.PrimaryKeyRelatedField(source='compra', read_only=True)
    libro_id = serializers.PrimaryKeyRelatedField(source='libro', read_only=True)

    class Meta:
        model = DetalleCompra
        fields = ['id', 'compra_id', 'libro_id', 'libro_titulo', 'precio']


class DetalleCompraCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleCompra
        fields = ['compra', 'libro', 'precio']

    def validate(self, attrs):
        user = self.context['request'].user
        compra = attrs.get('compra')

        if compra.usuario != user:
            raise serializers.ValidationError("No puedes agregar detalles a una compra que no es tuya.")
        return attrs



class DetalleCompraViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = DetalleCompra.objects.select_related('libro', 'compra')  # base queryset

    def get_queryset(self):
        return self.queryset.filter(compra__usuario=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return DetalleCompraCreateSerializer
        return DetalleCompraSerializer

