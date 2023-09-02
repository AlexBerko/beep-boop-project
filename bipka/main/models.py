from django.contrib.auth.models import *
from user.models import CustomUser

class Help(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=False)
    full_info = models.TextField(blank=False)
    who_asked = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, related_name='my_requests')
    who_complete = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL, blank=True, related_name='my_completed')
    pub_date = models.DateTimeField(auto_now_add=True)
    deadline_date = models.DateTimeField(null=True, blank=True)
    complete_date = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    #image = models.ImageField(upload_to='images') # можно добавить изображение к просьбе

    def __str__(self):
        return self.title