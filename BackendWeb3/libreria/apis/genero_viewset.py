from rest_framework import viewsets, serializers
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response

from libreria.models import Genero, Libro


class GeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genero
        fields = ['id', 'nombre']


class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = ['id', 'titulo', 'autor', 'precio', 'isbn', 'descripcion', 'foto']


class GeneroViewSet(viewsets.ModelViewSet):
    queryset = Genero.objects.all()
    serializer_class = GeneroSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'libros']:
            return [AllowAny()]
        permission_classes = [AllowAny]

    @action(detail=True, methods=['get'])
    def libros(self, request, pk=None):
        genero = self.get_object()
        libros = genero.libros.all()
        serializer = LibroSerializer(libros, many=True)
        return Response(serializer.data)
