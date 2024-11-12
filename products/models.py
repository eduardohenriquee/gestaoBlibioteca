# products/models.py
from django.db import models

class Product(models.Model):
    name = models.CharField('Name', max_length=100)
    description = models.TextField('Description', blank=True)
    price = models.DecimalField('Price', decimal_places=2, max_digits=8)
    created = models.DateTimeField('Created', auto_now_add=True)
    changed = models.DateTimeField('Changed', auto_now=True)
    available = models.BooleanField(default=True)
    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('emprestado', 'Emprestado'),
        ('em_manutencao', 'Em Manutenção'),
        ('indisponivel', 'Indisponível'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='disponivel'
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return reverse('product_edit', kwargs={'pk': self.pk})