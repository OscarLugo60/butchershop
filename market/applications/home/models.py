from model_utils.models import TimeStampedModel


from django.db import models

# Create your models here.

class Cliente(TimeStampedModel):
    name = models.CharField('Nombre', max_length=25)
    last_name = models.CharField('Apellido', max_length=25)
    identification = models.CharField('Identificación', max_length=9)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.name