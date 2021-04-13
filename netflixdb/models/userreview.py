from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class UserReview(models.Model):
    show = models.ForeignKey(to='Show', on_delete=models.CASCADE)
    user = models.ForeignKey(to='User', on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        constraints= [models.UniqueConstraint(fields=['show','user'],name='unique_review')]

    def __str__(self):
        return f"show {self.show}, user: {self.user}, rating:{self.rating}, review:{self.review}"