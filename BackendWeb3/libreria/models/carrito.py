from django.db import models

from libreria.models.libro import Libro
from libreria.models.usuario import Usuario


class Carrito(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='carrito')
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='libro')

    class Meta:
        unique_together = ('usuario', 'libro')
        verbose_name = 'Carrito'
        verbose_name_plural = 'Carritos'
        ordering = ['usuario', 'libro']

    def __str__(self):
        return f"{self.usuario.username} - {self.libro.titulo}"