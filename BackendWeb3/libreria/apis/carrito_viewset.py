from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated
from libreria.models.carrito import Carrito
from libreria.models.libro import Libro


class CarritoSerializer(serializers.ModelSerializer):
    libro_id = serializers.PrimaryKeyRelatedField(source='libro', queryset=Libro.objects.all())
    libro_titulo = serializers.CharField(source='libro.titulo', read_only=True)
    libro_precio = serializers.DecimalField(source='libro.precio', max_digits=10, decimal_places=2, read_only=True)
    libro_autor = serializers.CharField(source='libro.autor', read_only=True)
    libro_foto = serializers.ImageField(source='libro.foto', read_only=True)

    class Meta:
        model = Carrito
        fields = [
            'id',
            'libro_id',
            'libro_titulo',
            'libro_autor',
            'libro_precio',
            'libro_foto',
        ]
        read_only_fields = ['id', 'libro_titulo', 'libro_autor', 'libro_precio', 'libro_foto']


class CarritoCreateSerializer(serializers.ModelSerializer):
    libro = serializers.PrimaryKeyRelatedField(queryset=Libro.objects.all())

    class Meta:
        model = Carrito
        fields = ['libro']

    def validate(self, attrs):
        request = self.context.get('request')
        usuario = request.user if request else None
        libro = attrs.get('libro')

        if usuario and Carrito.objects.filter(usuario=usuario, libro=libro).exists():
            raise serializers.ValidationError("Este libro ya está en tu carrito.")
        return attrs

    def create(self, validated_data):
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)


class CarritoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Carrito.objects.select_related('libro').filter(usuario=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return CarritoCreateSerializer
        return CarritoSerializer


