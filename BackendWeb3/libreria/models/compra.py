from django.db import models

from libreria.models.usuario import Usuario


class Compra(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='compras')
    fecha_c = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    confirmada = models.BooleanField(default=False)


    def __str__(self):
        return f"Compra #{self.id} - {self.usuario.username}"
