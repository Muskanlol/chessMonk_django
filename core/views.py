from django.shortcuts import render,redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *


# Create your views here.


def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return{
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegisterView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer  = RegisterSerializer(data= request.data)

        if serializer.is_valid():
            user = serializer.save()
            tokens = get_token_for_user(user)

            return Response({
                'message': 'Registration successful!',
                'tokens':  tokens
            },status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer._validated_data['user']
            tokens = get_token_for_user(user)
            return Response({
                'message':'Login Successful🥳',
                'tokens': tokens,
                'user': UserProfileSerializer(user).data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

def home(request):
    return render(request, 'index.html')



