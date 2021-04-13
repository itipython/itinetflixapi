from django.db import models



class ShowHistory(models.Model):
    user = models.ForeignKey(to='User', on_delete=models.CASCADE , null=True, blank=True)
    show = models.ForeignKey(to='Show', on_delete=models.CASCADE , null=True, blank=True)
    watchDate = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f"id:{self.pk}, user:{self.user.username}, showID:{self.show.pk}, show:{self.show.name}, watchdate:{self.watchDate}"

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user','show'],name='unique_showhistory')]
        