from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Entrada(models.Model):
	titulo=models.CharField(max_length=100)
	contenido = models.TextField()
	fecha = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.titulo+" "+self.contenido[:20]

class Comentario(models.Model):
	fechacreacion=models.DateTimeField(auto_now_add=True)
	autor= models.CharField(max_length=100)
	mensaje = models.TextField()
	identrada = models.ForeignKey(Entrada)

	def __str__(self):
		return str("%s %s " % (self.identrada, self.mensaje[:60]))
