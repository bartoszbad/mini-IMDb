from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class MovieSearchClass(object):
    def __init__(self, title=None, types=None):
        self.title = title
        self.types = types


TYPES = [
    ("movie", "movie"),
    ("series", "series"),
    ("episode", "episode")
]

LISTS = [
    ("Favourites", "Favourites"),
    ("Want to see", "Want to see")
]


class Movie(models.Model):
    title = models.CharField(max_length=255, unique=True)
    year = models.CharField(null=True, max_length=255)  # is char because sometimes year cannot be parsed to int
    rated = models.CharField(max_length=10, null=True)
    released = models.CharField(max_length=255,
                                null=True)  # using char field because not sure if it keeps date format everytime
    runtime = models.CharField(max_length=255, null=True)
    genre = models.CharField(max_length=255, null=True)
    director = models.TextField(null=True)
    writer = models.TextField(null=True)
    actors = models.TextField(null=True)
    plot = models.TextField(null=True)
    language = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)
    awards = models.TextField(null=True)
    poster = models.TextField(null=True)
    metascore = models.CharField(max_length=255, null=True)
    imdbrating = models.CharField(max_length=255, null=True)
    imdbvotes = models.CharField(max_length=255, null=True)
    imdb_id = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=255, choices=TYPES)
    dvd = models.CharField(max_length=255,
                           null=True)  # using char field because not sure if it keeps date format everytime
    boxoffice = models.CharField(max_length=255, null=True)
    production = models.TextField(null=True)
    website = models.TextField(null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class UserMovieList(models.Model):
    name = models.CharField(max_length=128, choices=LISTS)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lists')

    def __str__(self):
        return f"{self.user} list name: {self.name}"


class MovieOnList(models.Model):
    list = models.ForeignKey(UserMovieList, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class MovieRating(models.Model):
    rating = models.IntegerField(validators=[MinValueValidator(1),
                                             MaxValueValidator(10)])
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')

    def __str__(self):
        return f"{self.user}, {self.movie}"
