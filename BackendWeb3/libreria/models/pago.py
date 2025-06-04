from django.db import models

from libreria.models.compra import Compra


class Pago(models.Model):
    compra = models.OneToOneField(Compra, on_delete=models.CASCADE, related_name='pago')
    qr = models.ImageField(upload_to='qr/', null=True, blank=True)
    pago_realizado = models.ImageField(upload_to='pagos/')
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"

    def __str__(self):
        return f"Pago de la compra #{self.compra.id}"