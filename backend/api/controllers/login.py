from rest_framework import status, viewsets, permissions
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from api.usecase.login.serializers import UserSerializer, UserLoginSerializer, UserPagination, UserFilter, UserLoginRefreshTokenSerializer, UserSerializerCreated

class LoginViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = UserPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter
    
    def get_permissions(self):
        if self.action in ['list']:
            return [permissions.IsAuthenticated()]
        elif self.action in ['create', 'login', 'logout', 'refresh_token', 'partial_update']:
            return [permissions.AllowAny()]
        elif self.action in ['update', 'destroy', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()
    
    def partial_update(self, request, *args, **kwargs):
        return Response(
            {"detail": "PATCH method is not allowed for this endpoint."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    @action(methods=['POST'], detail=False, url_path='login', url_name='login', serializer_class=UserLoginSerializer)
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(User, username=username)
        if not user.check_password(password):
            return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
        token, created = Token.objects.get_or_create(user=user)
        if created:
            token.save()
        serializer = UserSerializer(user, many=False)
        
        return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_200_OK)
    
    @action(methods=['DELETE'], detail=False, url_path='logout', url_name='logout')
    def logout(self, request):
        token = request.auth
        if token is not None:
            try:
                token.delete()
                return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
            except Token.DoesNotExist:
                return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "No token provided."}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['POST'], detail=False, url_path='refresh-token', url_name='refresh_token', serializer_class=UserLoginRefreshTokenSerializer)
    def refresh_token(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({"error": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

        # Delete the old token
        old_token = Token.objects.filter(user=user).first()
        if old_token:
            old_token.delete()

        # Create a new token
        new_token = Token.objects.create(user=user)
        new_token.save()
        return Response({"token": new_token.key}, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data['password']
        if not username or not password or not email:
            return Response({"error": "Username, Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserSerializerCreated(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()

            token = Token.objects.create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk):
        self.check_permissions(request)
        if request.user.id is pk:
           return Response({"error": "You do not have permission to update this user."}, status=status.HTTP_403_FORBIDDEN)
        
        password = request.data['password']
        username = request.data['username']
        email = request.data['email']
        user = get_object_or_404(User, pk=pk)
        user_equal = User.objects.filter(username=username).first()
        if user_equal and user.id != user_equal.id:
            return Response({"error": "A user with that username already exists."}, status=status.HTTP_400_BAD_REQUEST)
        user.username = username
        user.email = email
        if password:
            user.set_password(password)
        user.save()
        # Optionally delete the old token and create a new one
        Token.objects.filter(user=user).delete()  # This deletes all tokens for this user
        new_token = Token.objects.create(user=user)
        new_token.save()
        new_serializer = UserSerializer(user, many=False)
        return Response({"token": new_token.key, "user": new_serializer.data}, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk):
        self.check_permissions(request)
        if request.user.id != pk:
            return Response({"error": "You do not have permission to delete this user."}, status=status.HTTP_403_FORBIDDEN)

        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def retrieve(self, request, pk=None):
        self.check_permissions(request)

        if request.user.id != int(pk):
            return Response({"error": "You do not have permission to view this user."}, status=status.HTTP_403_FORBIDDEN)

        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)