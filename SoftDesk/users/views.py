from .models import User
from rest_framework import status
from .serializers import UserSerializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(APIView):
    def post(self, request):
        # Serialize the user data from the request
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            # Check if the user has given consent
            has_consent = serializer.validated_data.get('has_consent')
            if not has_consent:
                return Response(
                    {'error_message': 'Consent is required to register.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = serializer.save()
            return Response(
                {'message': 'User created successfully', 'user_id': user.id},
                status=status.HTTP_201_CREATED
            )
        else:
            # Return a response with validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        # Get emai and password from the request data
        email = request.data.get('email')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(email=email, password=password)

        if user is not None:
            # User is valid, generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            return Response({
                'message': 'Login successful',
                'access_token': str(access_token),
                'refresh_token': str(refresh),
                'user_id': user.id,
                'email': user.email,
            }, status=status.HTTP_200_OK)
        else:
            # User authentication failed
            return Response(
                {'error_message': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )


class UserViewSet(ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserView(APIView):
    # Requires authentication to access these endpoints
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve the authenticated user's information.
        """
        user_data = {
            'id': request.user.id,
            'username': request.user.username,
            'email': request.user.email,
            'age': request.user.age,
        }
        return Response(user_data, status=status.HTTP_200_OK)

    def put(self, request):
        # Update the authenticated user's information
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'User information updated successfully'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request):
        # Delete the authenticated user's account
        request.user.delete()
        return Response(
            {'message': 'User account deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )


class LogoutView(APIView):
    # Requires authentication to access these endpoints
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Get the user's refresh token from the request (optional)
        refresh_token = request.data.get('refresh_token')
        # Revoke the user's refresh token
        if refresh_token:

            try:
                RefreshToken(refresh_token).blacklist()
                return Response(
                    {'message': 'User has been logged out'},
                    status=status.HTTP_200_OK
                )

            except Exception:
                return Response(
                    {'error_message': 'Invalid refresh token'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {'message': 'Refresh token is required for logout'},
                status=status.HTTP_400_BAD_REQUEST
            )
