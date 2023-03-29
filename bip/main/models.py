from django.db import models

# Create your models here.
class Desk(models.Model):
    title = models.CharField('Краткое описание', max_length=255)

    def __str__(self):
        return self.title
