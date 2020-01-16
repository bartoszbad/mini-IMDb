"""myomdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from omdbapi.views import MovieSearchByTitleAndYear, MovieList, MovieDetail, MovieHighlight, \
    AddMovieToFavourites, RateMovie, RateMovieDetail, RateMovieDetailHighlight, FavouriteDetail, \
    FavouriteDetailHighlight, AddMovieToWantToSeeList, WantToSeeDetail, WantToSeeDetailHighlight, NewestMovies

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
