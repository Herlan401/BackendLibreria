from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id', 'email', 'es_administrador')

class UsuarioRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('email', 'password', 'es_administrador')
        extra_kwargs = {
            'email': {'required': True},
            'password': {'write_only': True, 'required': True},
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class UsuarioViewSet(viewsets.ViewSet):
    def get_permissions(self):
        if self.action in ['register', 'list']:
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(methods=['post'], detail=False, url_path='register')
    def register(self, request):
        serializer = UsuarioRegisterSerializer(data=request.data)
        if serializer.is_valid():
            usuario = serializer.save()
            return Response({
                'id': usuario.id,
                'email': usuario.email
            }, status=201)
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)

    def list(self, request):
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)

