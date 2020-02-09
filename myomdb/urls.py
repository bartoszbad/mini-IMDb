from django.contrib import admin
from django.urls import path, include

from omdbapi.views import AddMovieToFavourites, AddMovieToWantToSeeList, FavouriteDetail, FavouriteDetailHighlight, \
    MovieSearchByTitleAndYear, MovieList, MovieDetail, MovieHighlight, NewestMovies, RateMovie, RateMovieDetail, \
    RateMovieDetailHighlight, WantToSeeDetail, WantToSeeDetailHighlight

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('register_users.urls')),
    path('movies-by-title/', MovieSearchByTitleAndYear.as_view(), name='movie-by-title'),
    path('movies/', MovieList.as_view(), name='movie-list'),
    path('movies/<int:pk>/', MovieDetail.as_view(), name='movie-detail'),
    path('movies/<int:pk>/', MovieHighlight.as_view(), name='movie-highlight'),
    path('favourites-movies/', AddMovieToFavourites.as_view()),
    path('favourites-movies/<int:pk>/', FavouriteDetail.as_view()),
    path('favourites-movies/<int:pk>/', FavouriteDetailHighlight.as_view(), name='favourites-highlight'),
    path('wanted-movies/', AddMovieToWantToSeeList.as_view()),
    path('wanted-movies/<int:pk>/', WantToSeeDetail.as_view()),
    path('wanted-movies/<int:pk>/', WantToSeeDetailHighlight.as_view(), name='wanted-highlight'),
    path('rate/', RateMovie.as_view()),
    path('rate/<int:pk>/', RateMovieDetail.as_view()),
    path('rate/<int:pk>/', RateMovieDetailHighlight.as_view(), name='rate-highlight'),
    path('newest/', NewestMovies.as_view()),
]
