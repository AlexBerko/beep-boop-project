from django.db import models


class Help(models.Model):
    title = models.CharField('Краткое описание', max_length=255)
    full_info = models.TextField('Подробное описание')
    org_info = models.TextField('Описание организации')

    def __str__(self):
        return self.title
