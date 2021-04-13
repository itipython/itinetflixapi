from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=70, unique=True)
    
    def __str__(self):
        return f"{self.pk} : {self.name}"