from rest_framework import viewsets

from api.serializers import *
from netflixdb.models import *

# routerAdmin = routers.DefaultRouter()
# routerAdmin.register('user', views.UserFullViewSet)
# routerAdmin.register('users', views.UserViewSet)
# routerAdmin.register('reviews', views.UserReviewViewSet)
# routerAdmin.register('history', views.ShowHistoryViewSet)
# routerAdmin.register('playlist', views.ShowPlaylistViewSet)

# path('api/admin/', include(routerAdmin.urls)),





class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
  


class UserReviewViewSet(viewsets.ModelViewSet):

    queryset = UserReview.objects.all()
    serializer_class = UserReviewSerializer


class ShowHistoryViewSet(viewsets.ModelViewSet):

    queryset = ShowHistory.objects.all()
    serializer_class = ShowHistorySerializer



class ShowPlaylistViewSet(viewsets.ModelViewSet):

    queryset = ShowPlaylist.objects.all()
    serializer_class = ShowPlaylistSerializer


class UserFullViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserFullSerializer
