
from rest_framework import serializers
from django.contrib.auth import get_user_model


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = get_user_model()
        fields =  ('email', 'user_name', 'password', 'password2',)
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def password_validation(self, password):
        return get_user_model().is_strong_password(password)

    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError(
                {'error': 'passwords did not match'})

        user = get_user_model()(email=self.validated_data['email'],
                    user_name=self.validated_data['user_name'])
        user.set_password(self.validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'user_name', 'email']
