from django.shortcuts import redirect
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from django.conf import settings

from rest_framework.decorators import api_view, permission_classes


from django.core.mail import send_mail
from django.urls import reverse

from api.serializers import *
from netflixdb.models import *

# Create your views here.

### api v2

##signup
@api_view(['POST'])
def userSignup(request):

    serializeredUser = UserSerializer(data=request.data)
    if serializeredUser.is_valid():
        user =  User.objects.create(**serializeredUser.validated_data)
        user.set_password(user.password)
        user.save()
        return Response(
                {
                "user":UserSerializer(user).data
                }, status=status.HTTP_201_CREATED
            )
    else:
        return Response(
            {
                "errors":serializeredUser.errors
            }, status=status.HTTP_400_BAD_REQUEST
        )


###login and authentication
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        if user.isVerified:
            serializeredUser = UserSerializer(User.objects.get(username=user.username))
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'username': user.username,
                'user':serializeredUser.data,
            }, status=status.HTTP_200_OK)
          
        else:
            send_mail("Verify Your Account ITI-PYTHON-FullStack", 
                    f''' Thank you for registeration on ITI-PYTHON-FullStack to verify your account click on the link below...
                        Thanks, 
                        ITI-PYTHON-TEAM 
                        "{request.build_absolute_uri(reverse('verifyUserViaEmail',kwargs={"tk":token}))}"  
                            '''
                    , settings.EMAIL_HOST_USER,
                    [token.user.email],
                        )
            return Response(
                {
                    "message":f"non-verified user, please check your email: {user.email} to verify your account."
                }, status= status.HTTP_401_UNAUTHORIZED
            )

userLogin = CustomAuthToken.as_view() 


### email verification
@api_view(['GET','POST'])
def verifyUserViaEmail(request, tk):
    try:
        token = Token.objects.get(key=tk)
    except Token.DoesNotExist:
        return Response(status= status.HTTP_404_NOT_FOUND)
    
    user = User.objects.get(auth_token=tk)
    user.isVerified = True
    user.save()
    return redirect(settings.FRONT_END__SITEURL)

### reset user password via email
@api_view(['GET','POST'])
def resetUserPassword(request):
    if request.data.get('username') or request.data.get("email"):
        user = User.objects.get(username=request.data.get('username')) if request.data.get('username') else User.objects.get(email=request.data.get('email'))
        try:
             token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            return Response(status= status.HTTP_404_NOT_FOUND)

        send_mail("Reset Your password for ITI-PYTHON-FullStack", 
                    f''' hello {user.username}, we got your request to reset your password please click the link below it will redirect you to our site to enter your new password...
                        Thanks, 
                        ITI-PYTHON-TEAM 
                        "{settings.FRONT_END__SITEURL}/resetpassword/?tk={token}"  
                            '''
                    , settings.EMAIL_HOST_USER,
                    [token.user.email],
                        )
        return Response(
            {"success":f"please check you inbox"}
            )
    
    else:
        return Response(
                {
                    "error":"please provide an username or password"
                }
                ,status=status.HTTP_400_BAD_REQUEST
            )




###user profile and full information
@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def getUserInfo(request):

    try:
        serializereddUser = UserFullSerializer(User.objects.get(pk=request.user.pk))

    except User.DoesNotExist:
        return Response(status= status.HTTP_404_NOT_FOUND)

    return Response(
            {
            "user":serializereddUser.data
            }, status=status.HTTP_200_OK
        )
    


##update userInfo

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def updateUserInfo(request):
    
    serializeredUser = UserFullSerializer(data=request.data, partial=True)

    try:
        user =  serializeredUser.update(User.objects.get(pk=request.user.pk), validated_data=request.data)
      
        if  request.data.get('password'):
                user.set_password(user.password)
                user.save()
        return Response(
                    {
                    "user":UserFullSerializer(User.objects.get(pk=request.user.pk)).data
                    }, status=status.HTTP_200_OK
                )
        
    except:
        serializeredUser.is_valid()
        return Response(
            {
                "errors":serializeredUser.errors
            }, status=status.HTTP_400_BAD_REQUEST
        )


##show full info
@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def getShowInfo(request):

    try:
        serializereddShow = ShowFullSerializer(Show.objects.get(pk=request.data.get("showID")))

    except Show.DoesNotExist:
        return Response(status= status.HTTP_404_NOT_FOUND)

    myReview = ""
    for review in serializereddShow.data.get("userReviews"):
        if review["user"] == request.user.username:
            myReview = review
            break
    User.objects.filter(id=request.user.pk).update(currentShow = Show.objects.get(pk=request.data.get("showID")))
    show, created = ShowHistory.objects.update_or_create(user=request.user, show=Show.objects.get(pk=request.data.get("showID")))
    return Response(
            {
            "Show" : serializereddShow.data,
            "MyReview" : myReview
            }, status=status.HTTP_200_OK
        )
        



### show dashboard 

class ShowViewSet(viewsets.ModelViewSet):

    queryset = Show.objects.all()
    serializer_class = ShowSerializer
    permission_classes=[IsAuthenticated]
    http_method_names = ['get']


### reviews
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def getAllReviews(request):
    if UserReview.objects.filter(show__id=request.data.get("showID")).count() > 0:

            return Response(
                        {
                        "reviews":UserReviewSerializer(UserReview.objects.filter(show__id=request.data.get("showID")),many=True).data
                        }, status=status.HTTP_201_CREATED
                    )
    else:
        
        return Response(
            {"error":"no reviews for this show"},status=status.HTTP_404_NOT_FOUND
        )
    


###create update userreview
@api_view(["POST", "DELETE"])
@permission_classes([IsAuthenticated])
def CRUDUserReview(request):
    if request.method == "POST":

        if UserReview.objects.filter(user__id=request.user.pk, show__id=request.data.get("showID")).count() == 0:

            serializeredUserReview = UserReviewSerializer(data=request.data)
            if serializeredUserReview.is_valid():
                userReview =  UserReview.objects.create(user=request.user, show=Show.objects.get(id=request.data.get("showID")),**serializeredUserReview.validated_data)
               
                return Response(
                        {
                        "myReview":UserReviewSerializer(userReview).data
                        }, status=status.HTTP_201_CREATED
                    )
            else:
                return Response(
                    {
                        "errors":serializeredUserReview.errors
                    }, status=status.HTTP_400_BAD_REQUEST
                )           


        else:
            serializeredUserReview = UserReviewSerializer(data=request.data, partial=True)
        
            if  serializeredUserReview.is_valid():
                userReview =  serializeredUserReview.update(UserReview.objects.get(user__id=request.user.pk, show__id=request.data.get("showID")), validated_data=request.data)
                return Response(
                            {
                            "myReview":UserReviewSerializer(userReview).data
                            }, status=status.HTTP_200_OK
                        )
                
            else:
                return Response(
                    {
                        "errors":serializeredUserReview.errors
                    }, status=status.HTTP_400_BAD_REQUEST
                )


    if request.method == "DELETE":
        try:
            myReview = UserReview.objects.get(user=request.user, show__id= request.data.get('showID'))
            myReview.delete()
            return Response(
                            {
                            "myReview":UserReviewSerializer(myReview).data
                            }, status=status.HTTP_204_NO_CONTENT
                        )
                
        except:
            return Response(
                    {
                        "errors":f"{request.user.username} doesn't reviewed show with id:{request.data.get('showID')}"
                    }, status=status.HTTP_400_BAD_REQUEST
                )



### playlist


###create update playlist
@api_view(["POST", "DELETE"])
@permission_classes([IsAuthenticated])
def CRUDShowPlaylist(request):
    if request.method == "POST":

            serializeredPlayList = ShowPlaylistSerializer(data=request.data)
            if serializeredPlayList.is_valid():
                show, created =  ShowPlaylist.objects.update_or_create(user=request.user, show=Show.objects.get(id=request.data.get("showID")),**serializeredPlayList.validated_data)
               
                return Response(
                        {
                        "show":ShowPlaylistSerializer(show).data
                        }, status=status.HTTP_201_CREATED
                    )
            else:
                return Response(
                    {
                        "errors":serializeredPlayList.errors
                    }, status=status.HTTP_400_BAD_REQUEST
                )           


                

    if request.method == "DELETE":
        try:
            showplaylist = ShowPlaylist.objects.get(user=request.user, show__id= request.data.get('showID'))
            showplaylist.delete()
            return Response(
                            {
                            "show":ShowPlaylistSerializer(showplaylist).data
                            }, status=status.HTTP_204_NO_CONTENT
                        )
                
        except:
            return Response(
                    {
                        "errors":f"{request.user.username} doesn't have show with id:{request.data.get('showID')} on his playlist"
                    }, status=status.HTTP_400_BAD_REQUEST
                )



### history


###delete show history
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteShowHistory(request):

  if request.method == "DELETE":
    if request.data.get("AllHISTORY") == "true" :
        showHistory = ShowHistory.objects.filter(user=request.user).delete()
        return Response(
            {
                "success":f"clear all shows history for {request.user.username}"
            },status=status.HTTP_200_OK
        )

    try:
        showHis = ShowHistory.objects.get(user=request.user, show__id= request.data.get('showID'))
        showHis.delete()
        return Response(
                        {
                        "show":ShowHistorySerializer(showHis).data
                        }, status=status.HTTP_204_NO_CONTENT
                    )
            
    except:
        return Response(
                {
                    "errors":f"{request.user.username} doesn't have show with id:{request.data.get('showID')} on his history"
                }, status=status.HTTP_400_BAD_REQUEST)








### api v1 
### admin api




class GenreViewSet(viewsets.ModelViewSet):

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class ProducerViewSet(viewsets.ModelViewSet):

    queryset = Producer.objects.all()
    serializer_class = ProducerSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class AuthorViewSet(viewsets.ModelViewSet):

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class ActorViewSet(viewsets.ModelViewSet):

    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class PrizeViewSet(viewsets.ModelViewSet):

    queryset = Prize.objects.all()
    serializer_class = PrizeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class ShowFullViewSet(viewsets.ModelViewSet):

    queryset = Show.objects.all()
    serializer_class = ShowFullSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]



class MembershipViewSet(viewsets.ModelViewSet):

    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

