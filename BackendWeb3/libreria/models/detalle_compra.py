from django.db import models

from libreria.models.compra import Compra
from libreria.models.libro import Libro


class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='items')
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=8, decimal_places=2, null=False)

    class Meta:
        verbose_name = 'Detalle de Compra'
        verbose_name_plural = 'Detalles de Compra'
        ordering = ['compra', 'libro']

    def __str__(self):
        return f"{self.libro.titulo} comprado por {self.compra.usuario.username}"