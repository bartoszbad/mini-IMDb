from django.contrib.auth.models import User
from django.shortcuts import render
import datetime
from rest_framework import generics, status, renderers, request
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Movie, MovieRating, MovieOnList
from .permissions import IsOwnerOrReadOnly
from .serializers import MovieSerializer, MovieSearchByTitleSerializer, \
    MovieRatingSerializer, MovieOnListSerializer


# Explore movie database
class MovieList(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class MovieDetail(generics.RetrieveDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAdminUser]


# link to movie details
class MovieHighlight(generics.GenericAPIView):
    queryset = Movie.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        movie = self.get_object()
        return Response(movie.highlighted)


# Search movie by title, omdb returns one closest match
class MovieSearchByTitleAndYear(generics.ListAPIView):
    queryset = Movie.objects.none()
    serializer_class = MovieSearchByTitleSerializer

    def post(self, request):
        serializer = MovieSearchByTitleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serialized_movie = serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serialized_movie.data, status=status.HTTP_201_CREATED)


class AddMovieToFavourites(generics.ListCreateAPIView):
    serializer_class = MovieOnListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MovieOnList.objects.filter(user=self.request.user).filter(list__name="Favourites")

    def perform_create(self, serializer):
        user = self.request.user
        fav_list = user.lists.get(name="Favourites")
        # prevent duplicates
        if len(MovieOnList.objects.filter(user=user).filter(movie=self.request.data['movie']).filter(list=fav_list)) > 0:
            raise ValidationError("You have already added this movie to that list!")
        return serializer.save(user=user, list=fav_list)


class FavouriteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MovieOnList.objects.all()
    serializer_class = MovieOnListSerializer
    permission_classes = [IsOwnerOrReadOnly]


# link to details of Favourite
class FavouriteDetailHighlight(generics.GenericAPIView):
    queryset = MovieOnList.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        favourite = self.get_object()
        return Response(favourite.highlighted)


class AddMovieToWantToSeeList(generics.ListCreateAPIView):
    serializer_class = MovieOnListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MovieOnList.objects.filter(user=self.request.user).filter(list__name="Want to see")

    def perform_create(self, serializer):
        user = self.request.user
        want_list = user.lists.get(name="Want to see")
        # prevent duplicates
        if len(MovieOnList.objects.filter(user=user).filter(movie=self.request.data['movie']).filter(list=want_list)) > 0:
            raise ValidationError("You have already added this movie to that list!")
        return serializer.save(user=user, list=want_list)


class WantToSeeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MovieOnList.objects.all()
    serializer_class = MovieOnListSerializer
    permission_classes = [IsOwnerOrReadOnly]


# link to details of Want to see movie
class WantToSeeDetailHighlight(generics.GenericAPIView):
    queryset = MovieOnList.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        wanted = self.get_object()
        return Response(wanted.highlighted)


class RateMovie(generics.ListCreateAPIView):
    serializer_class = MovieRatingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MovieRating.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # prevent duplicates
        if len(MovieRating.objects.filter(user=self.request.user).filter(movie=self.request.data['movie'])) > 0:
            raise ValidationError("You have already rated this movie!")
        return serializer.save(user=self.request.user)


class RateMovieDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MovieRating.objects.all()
    serializer_class = MovieRatingSerializer
    permission_classes = [IsOwnerOrReadOnly]


# link to details of Movie Rating
class RateMovieDetailHighlight(generics.GenericAPIView):
    queryset = MovieRating.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        rate = self.get_object()
        return Response(rate.highlighted)


class NewestMovies(generics.ListAPIView):
    serializer_class = MovieSerializer

    def get_queryset(self):
        today = datetime.date.today()
        two_week_ago = today - datetime.timedelta(days=14)
        return Movie.objects.filter(date_added__gte=two_week_ago)
