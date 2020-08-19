from django.db import models

class Channel(models.Model):
    name = models.CharField(max_length=60, unique=True)
    def __str__(self):
        return self.name

class Message(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    content = models.CharField(max_length=60)
    user = models.CharField(max_length=60, default="itang")
    def __str__(self):
        return self.content

