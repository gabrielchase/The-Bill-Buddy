from django.db import models
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Service(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    
    def __str__(self):
        return self.name


class Bill(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField()
    due_date = models.IntegerField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return '{} - {}'.format(self.service, self.name)
