from django.db import models

class Membership(models.Model):
    name = models.CharField(max_length=70)
    duration = models.IntegerField()
    price = models.FloatField()


    class Meta:
        constraints= [models.UniqueConstraint(fields=['name','duration','price'],name='unique_membership')]

    def __str__(self):
        return f"id:{self.pk}, membership: {self.name}, price:{self.price}, duration:{self.duration} days"