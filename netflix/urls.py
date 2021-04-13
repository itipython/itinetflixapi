"""netflix URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from os import name
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api import views

from django.conf import settings
from django.conf.urls.static import static


routerAdmin = routers.DefaultRouter()
routerAdmin.register('genres', views.GenreViewSet)
routerAdmin.register('producers', views.ProducerViewSet)
routerAdmin.register('authors', views.AuthorViewSet)
routerAdmin.register('actors', views.ActorViewSet)
routerAdmin.register('prize', views.PrizeViewSet)
routerAdmin.register('shows', views.ShowFullViewSet)
routerAdmin.register('memberships', views.MembershipViewSet)

router = routers.DefaultRouter()
router.register('shows', views.ShowViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/admin/', include(routerAdmin.urls)),
    path('api/v2/users/signup/',views.userSignup, name="userSignup"),
    path('api/v2/users/login/',views.userLogin, name="userLogin"),
    path('api/v2/', include(router.urls), name="Dashboard"),
    path('api/v2/verifyUser/<str:tk>',views.verifyUserViaEmail, name="verifyUserViaEmail"),
    path('api/v2/resetpassword/',views.resetUserPassword, name="resetUserPassword"),
    path('api/v2/users/info',views.getUserInfo, name="userInfo"),
    path('api/v2/users/update',views.updateUserInfo, name="updateUser"),
    path('api/v2/shows/info',views.getShowInfo, name="showInfo"),
    path('api/v2/userreview/',views.CRUDUserReview, name="CRUDUserReview"),
    path('api/v2/reviews/',views.getAllReviews, name="getReview"),
    path('api/v2/showplaylist/',views.CRUDShowPlaylist, name="CRUDshowPlaylist"),
    path('api/v2/showhistory/',views.deleteShowHistory, name="DeleteShowHistory"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)