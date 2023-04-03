from django.db import models

# Create your models here.
class Help(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField('Краткое описание', max_length=255)
    full_info = models.TextField('Подробное описание')
    org_info = models.TextField('Описание организации')
    pubdate = models.DateTimeField('Дата публикации')

    def __str__(self):
        return self.title
