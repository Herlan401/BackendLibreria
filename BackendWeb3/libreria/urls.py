from django.urls import include, path
from rest_framework import routers

from libreria.apis import genero_viewset
from libreria.apis.compra_viewset import CompraViewSet
from libreria.apis.genero_viewset import GeneroViewSet
from libreria.apis.carrito_viewset import CarritoViewSet
from libreria.apis.detallecompra_viewset import DetalleCompraViewSet
from libreria.apis.libro_viewset import LibroViewSet
from libreria.apis.comprapago_viewset import PagoViewSet
from libreria.apis.usuario_viewset import UsuarioViewSet

router = routers.DefaultRouter()

router.register('carrito',CarritoViewSet,basename="carrito")
router.register('detallecompra',DetalleCompraViewSet,basename="detallecompra")
router.register('pago',PagoViewSet)
router.register('compra', CompraViewSet, basename='compra')

router.register('libro',LibroViewSet)
router.register('genero',GeneroViewSet)
router.register("auth",UsuarioViewSet,basename="auth")
urlpatterns = [
    path('',include(router.urls)),
]