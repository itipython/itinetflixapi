from django.db import models



class ShowPlaylist(models.Model):
    user = models.ForeignKey(to='User', on_delete=models.CASCADE, null=True, blank=True)
    show = models.ForeignKey(to='Show', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return f"userID:{self.user.pk}, user:{self.user.username}, showID:{self.show.pk}, show:{self.show.name}"

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user','show'],name='unique_showlist')]