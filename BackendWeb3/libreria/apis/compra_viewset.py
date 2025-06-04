from rest_framework import serializers, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, JSONParser

from libreria.models import Compra, Carrito, DetalleCompra, Libro


class LibroDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = ['id', 'titulo', 'precio']


class CompraSerializer(serializers.ModelSerializer):
    libros = serializers.SerializerMethodField()
    pago_realizado = serializers.SerializerMethodField()

    class Meta:
        model = Compra
        fields = ['id', 'monto_total', 'confirmada', 'fecha_c', 'libros', 'pago_realizado']

    def get_libros(self, obj):
        return LibroDetalleSerializer(
            [detalle.libro for detalle in obj.items.select_related('libro')],
            many=True
        ).data

    def get_pago_realizado(self, obj):
        return getattr(obj.pago.pago_realizado, 'url', None) if hasattr(obj, 'pago') else None


class CompraCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compra
        fields = []

    def create(self, validated_data):
        return self.context['view'].crear_compra_desde_carrito(self.context['request'])


class CompraViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, JSONParser]

    def get_queryset(self):
        return Compra.objects.filter(
            usuario=self.request.user,
            confirmada=True
        ).prefetch_related('items__libro')

    def get_serializer_class(self):
        return CompraCreateSerializer if self.action == 'create' else CompraSerializer

    def crear_compra_desde_carrito(self, request):
        usuario = request.user
        carrito_items = Carrito.objects.select_related('libro').filter(usuario=usuario)

        if not carrito_items.exists():
            raise serializers.ValidationError("El carrito está vacío.")

        monto_total = sum(item.libro.precio for item in carrito_items)
        compra = Compra.objects.create(usuario=usuario, monto_total=monto_total)

        detalles = [
            DetalleCompra(compra=compra, libro=item.libro, precio=item.libro.precio)
            for item in carrito_items
        ]
        DetalleCompra.objects.bulk_create(detalles)
        carrito_items.delete()

        return compra

    @action(detail=False, methods=['post'], url_path='crear-desde-carrito')
    def crear_desde_carrito(self, request):
        try:
            compra = self.crear_compra_desde_carrito(request)
        except serializers.ValidationError as e:
            return Response({'error': str(e.detail[0])}, status=status.HTTP_400_BAD_REQUEST)

        libros_comprados = [
            {'titulo': detalle.libro.titulo, 'precio': detalle.libro.precio}
            for detalle in compra.items.select_related('libro')
        ]

        qr_url = request.build_absolute_uri('/static/img/qr.png')

        return Response({
            'compra_id': compra.id,
            'monto_total': compra.monto_total,
            'libros': libros_comprados,
            'qr': qr_url
        }, status=status.HTTP_201_CREATED)

