from django.contrib import admin

from omdbapi.models import Movie, MovieRating

admin.site.register(Movie)
admin.site.register(MovieRating)
