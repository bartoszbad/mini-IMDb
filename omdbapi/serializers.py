import omdb
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Movie, UserMovieList, MovieRating, MovieOnList

TYPES = {
    "movie"
    "series"
    "episode"
}


class MovieSerializer(WritableNestedModelSerializer):
    details = serializers.HyperlinkedIdentityField(view_name='movie-highlight', format='html')

    class Meta:
        model = Movie
        fields = '__all__'


class MovieSerializerWithoutDetails(WritableNestedModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class MovieSearchByTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('title', 'year', 'type')

    def save(self, **kwargs):
        omdb.set_default('apikey', '4a41d844')
        omdb.set_default('tomatoes', True)
        movie_data = omdb.get(
            title=f"{self.validated_data['title']}",
            year=f"{self.validated_data['year']}",
            media_type=f"{self.validated_data['type']}",
            timeout=5
        )

        # Catch exception when movie does not exist in OMDB
        try:
            print(movie_data['title'])
        except KeyError:
            raise ValidationError("No such movie in OMDB.")

        # Does not allow creating duplicates
        if Movie.objects.filter(title=movie_data['title']).exists():
            raise ValidationError("Movie with this title already exists in database.")

        movie_serializer = MovieSerializerWithoutDetails(data=movie_data)
        if movie_serializer.is_valid():
            movie_serializer.save()
            return movie_serializer
        else:
            raise ValidationError(movie_serializer.errors)


class UserMovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMovieList
        fields = ['name', 'movies']


class MovieOnListSerializer(serializers.ModelSerializer):
    details = serializers.HyperlinkedIdentityField(view_name='favourites-highlight')

    class Meta:
        model = MovieOnList
        fields = ['details', 'movie']

    def to_representation(self, instance):
        """
        While listing movies from list it shows movie title not id
        """
        rep = super(MovieOnListSerializer, self).to_representation(instance)
        rep['movie'] = instance.movie.title
        return rep


class MovieRatingSerializer(serializers.ModelSerializer):
    details = serializers.HyperlinkedIdentityField(view_name='rate-highlight')

    class Meta:
        model = MovieRating
        exclude = ['user']

    def to_representation(self, instance):
        """
        In Rate List it shows movie title not id
        """
        rep = super(MovieRatingSerializer, self).to_representation(instance)
        rep['movie'] = instance.movie.title
        return rep
