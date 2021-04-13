from django.contrib import admin

from .models.user import User
from .models.show import Show
from .models.showhistory import ShowHistory
from .models.showplaylist import ShowPlaylist
from .models.userreview import UserReview
from .models.membership import Membership
from .models.prize import Prize
from .models.producer import Producer
from .models.author import Author
from .models.actor import Actor
from .models.genre import Genre

 



admin.site.register(User)
admin.site.register( Show)
admin.site.register( ShowHistory)
admin.site.register( ShowPlaylist)
admin.site.register( UserReview)
admin.site.register( Membership)
admin.site.register( Prize)
admin.site.register( Producer)
admin.site.register( Author)
admin.site.register( Actor)
admin.site.register( Genre)
