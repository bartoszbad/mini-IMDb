from django.contrib.auth.models import User
from rest_framework import serializers
from omdbapi.models import UserMovieList
from omdbapi.serializers import MovieRatingSerializer


class AddUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
        write_only_fields = ('password',)
        read_only_fields = ('is_staff', 'is_superuser', 'is_active', 'date_joined',)

    def create(self, validated_data, instance=None):
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
        )
        if self.validated_data['password'] != self.validated_data['password2']:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(validated_data['password'])
        user.save()
        UserMovieList.objects.create(name="Favourites", user=user)
        UserMovieList.objects.create(name="Want to see", user=user)
        return user


class UserSerializer(serializers.HyperlinkedModelSerializer):
    details = serializers.HyperlinkedIdentityField(view_name='user-highlight')

    class Meta:
        model = User
        fields = ['id', 'details', 'username']


class UserDetailSerializer(serializers.HyperlinkedModelSerializer):
    details = serializers.HyperlinkedIdentityField(view_name='user-highlight')
    ratings = MovieRatingSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'details', 'username', 'ratings']


