from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.template.defaultfilters import length


class Show(models.Model):

    name = models.CharField(max_length=70)
    productionDate = models.DateField()
    rate = models.FloatField(default=3, validators=[MinValueValidator(1), MaxValueValidator(5)])
    userReviews = models.ManyToManyField(to='User', related_name='reviews', related_query_name='review', through='UserReview',  through_fields=('show','user'), blank=True)
    parentGuide = models.CharField(max_length=1,choices=[('a',"adults"),('c','childern')])
    videoURL = models.URLField(max_length=2048 )
    posterURL = models.URLField(max_length=2048 )
    description = models.TextField()
    language = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    genres = models.ManyToManyField(to='Genre')
    prizes = models.ManyToManyField(to='Prize', blank=True)
    authors = models.ManyToManyField(to='Author')
    producers = models.ManyToManyField(to='Producer')
    actors = models.ManyToManyField(to='Actor')


    def __str__(self):
        return f"id: {self.pk}, name:{self.name}"