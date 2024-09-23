from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.views import check_existing_email
from .serializers import PlayerSerializer, UserRegistrationSerializer, ResetPasswordSerializer, LoginSerializer
from players.models import Player
from user.models import CustomUser
from django.core.mail import send_mail
from django.conf import settings
from authentication.views import check_existing_email




# Handles listing and creating players
class PlayerListView(APIView):
    def get(self, request):
        players = Player.objects.all()
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PlayerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Handles retrieval, update, and deletion of a single player
class PlayerDetailView(APIView):
    def get(self, request, player_id):
        player = get_object_or_404(Player, pk=player_id)
        serializer = PlayerSerializer(player)
        return Response(serializer.data)

    def put(self, request, player_id):
        player = get_object_or_404(Player, pk=player_id)
        serializer = PlayerSerializer(player, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterUser(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        # Check if the serializer is valid
        if serializer.is_valid():
            user = serializer.save()
            response_data = {
                'message': f"{user.role.capitalize()} {user.first_name} {user.last_name} successfully created",
                 'user': {
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'role': user.role,
                }
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginUser(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)
            if user:
                auth_login(request, user)
                return Response({'detail': 'Login successful'}, status=status.HTTP_200_OK)
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Reset Password View
class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = CustomUser.objects.filter(email=email).first()
            if user:
                send_mail(
                    'Password Reset Request',
                    'Follow the link to reset your password.',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                )
                return Response({'detail': 'Password reset email sent'}, status=status.HTTP_200_OK)
            return Response({'detail': 'Email not found'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# User List View
class UserListView(APIView):
    def get(self, request):
        users = CustomUser.objects.all()
        email = request.query_params.get("email")
        if email:
            users = users.filter(email=email)
        serializer = UserRegistrationSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# User Detail View
class UserDetailView(APIView):
    def get(self, request, id):
        user = get_object_or_404(CustomUser, id=id)
        serializer = UserRegistrationSerializer(user)
        return Response(serializer.data)

    def put(self, request, id):
        user = get_object_or_404(CustomUser, id=id)
        serializer = UserRegistrationSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        user = get_object_or_404(CustomUser, id=id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
