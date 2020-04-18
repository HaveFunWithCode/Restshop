from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth import logout
from rest_framework.viewsets import ViewSet, ModelViewSet

from .models import ShopUser, Adress
from .serializers import RegisterSerializer, LoginSerilizer, CustomerProfileSerializer, AddressSerializer


class RegisterView(CreateAPIView):
    serializer_class=RegisterSerializer


class ProfileView(APIView):
    # TODO: edit profile
    permission_classes =[IsAuthenticated]
    serializer_class=CustomerProfileSerializer
    def get(self,request):
        user = request.user
        return Response(self.serializer_class(user.customerProfile).data)

class AddressViewSet(ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Adress.objects.filter(user=self.request.user)

        
    def create(self, request, *args, **kwargs):
        current_user=request.user
        request.data['user']=current_user.id
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers=self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)
# TODO: should add check is_verified
class LoginAPIView(APIView):
    serializer_class=LoginSerilizer
    def post(self,request):

        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

class logoutView(APIView):
    def post(self,request):
        logout(request)
        return Response(data={'success':'Sucessfully logged out'},status=status.HTTP_200_OK)


def verifyemail(request, uuid):
    try:
        user = ShopUser.objects.get(verification_uuid=uuid, is_verified=False)
    except ShopUser.DoesNotExist:
        raise Http404("User does not exist or is already verified")
    user.is_verified = True
    user.save()
    return redirect('profile')


























