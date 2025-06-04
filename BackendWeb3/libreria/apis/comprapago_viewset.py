from rest_framework import serializers, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from libreria.models import DetalleCompra
from libreria.models.pago import Pago
from libreria.models.compra import Compra

class PagoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = ['compra', 'pago_realizado']

class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = ['id', 'compra', 'qr', 'pago_realizado', 'fecha']
        read_only_fields = ['qr', 'fecha']

class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Pago.objects.filter(compra__usuario=self.request.user)

    def get_serializer_class(self):
        return PagoCreateSerializer if self.action == 'create' else PagoSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        compra = serializer.validated_data['compra']

        if Pago.objects.filter(compra=compra).exists():
            return Response(
                {"error": "Ya existe un pago para esta compra."},
                status=status.HTTP_400_BAD_REQUEST
            )

        pago = serializer.save()

        compra.confirmada = True
        compra.save(update_fields=["confirmada"])

        detalles = DetalleCompra.objects.filter(compra=compra).select_related('libro')
        for item in detalles:
            item.libro.ventas += 1
            item.libro.save(update_fields=["ventas"])

        pago.qr = 'static/img/qr.png'
        pago.save(update_fields=["qr"])

        return Response(PagoSerializer(pago).data, status=status.HTTP_201_CREATED)
