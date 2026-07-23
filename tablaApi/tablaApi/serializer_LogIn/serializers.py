from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        
        if user and user.is_active:
            refresh = RefreshToken.for_user(user)
            # Inyectamos el rol en el token
            refresh.access_token['rol'] = str(user.rol)
            
            return {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'username': user.username,
                'rol': user.rol
            }
        raise serializers.ValidationError("Credenciales incorrectas")