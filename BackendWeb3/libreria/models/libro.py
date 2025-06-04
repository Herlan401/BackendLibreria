from django.db import models

from libreria.models.genero import Genero


class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    ventas = models.PositiveIntegerField(default=0)
    autor = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=5, decimal_places=2)
    isbn = models.CharField(max_length=13, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    foto = models.ImageField(upload_to='imagen')
    generos = models.ManyToManyField(Genero,related_name='libros')


    def __str__(self):
        return f"{self.titulo} by {self.autor}"