from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny
from rest_framework.response import Response

from libreria.models.libro import Libro
from libreria.models.genero import Genero

class GeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genero
        fields = ['id', 'nombre']

class LibroSerializer(serializers.ModelSerializer):
    generos = GeneroSerializer(many=True, read_only=True)

    class Meta:
        model = Libro
        fields = [
            'id', 'titulo', 'autor', 'precio', 'isbn', 'ventas',
            'descripcion', 'foto', 'generos'
        ]

class LibroCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = [
            'titulo',
            'autor',
            'precio',
            'isbn',
            'ventas',
            'descripcion',
            'foto',
            'generos'
        ]

class LibroViewSet(viewsets.ModelViewSet):
    queryset = Libro.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return LibroSerializer
        return LibroCreateSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticatedOrReadOnly()]
        return [AllowAny()]

    @action(detail=False, methods=['get'], url_path='por-genero/(?P<genero_id>[^/.]+)')
    def libros_por_genero(self, request, genero_id=None):
        try:
            genero = Genero.objects.get(id=genero_id)
            libros = Libro.objects.filter(generos=genero)
            serializer = self.get_serializer(libros, many=True)
            return Response(serializer.data)
        except Genero.DoesNotExist:
            return Response(
                {'error': 'Género no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )