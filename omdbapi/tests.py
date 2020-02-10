from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import RequestsClient, APIRequestFactory

from omdbapi.models import Movie, MovieRating
from omdbapi.serializers import MovieSerializer

client = RequestsClient()
request_factory = APIRequestFactory()


class TestMovieListView(TestCase):
    def setUp(self):
        Movie.objects.create(title='abc')
        Movie.objects.create(title='def')

    def test_request_client(self):
        response = self.client.get('/movies/')
        self.assertEqual(response.status_code, 200)

    def test_number_of_movies(self):
        self.assertEqual(Movie.objects.count(), 2)


class TestMovieDetail(TestCase):
    def setUp(self):
        Movie.objects.create(title='abc')
        Movie.objects.create(title='def')
        self.movie = Movie.objects.create(title='delete')

    def test_request_client(self):
        response = self.client.get('/movies/1/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/movies/10/')
        self.assertEqual(response.status_code, 404)

    def test_document_detail_view(self):
        movie = Movie.objects.get(id=1)
        response = self.client.get('http://127.0.0.1:8000/movies/{}/'.format(movie.pk))
        request = request_factory.get('/')
        serializer = MovieSerializer(movie, context={'request': request})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_anonymous_delete_method(self):
        response = self.client.delete(reverse('movie-detail', kwargs={'pk': self.movie.pk}))
        self.assertEqual(response.status_code, 403)


class TestMovieDetailByAdmin(TestCase):
    def setUp(self):
        Movie.objects.create(title='abc')
        Movie.objects.create(title='def')
        self.movie = Movie.objects.create(title='delete')
        self.username = 'admin'
        self.password = 'admin'
        self.user = User.objects.create_superuser(self.username, self.password)

    def test_document_put_method(self):
        movie = Movie.objects.get(title='def')
        movie.title = 'some_new_value'
        movie.save()
        self.assertEqual(movie.title, 'some_new_value')

    def test_admin_delete_method(self):
        self.client.force_login(user=self.user)
        response = self.client.delete('/movies/4/')
        self.assertEqual(response.status_code, 404)
        response = self.client.delete(reverse('movie-detail', kwargs={'pk': self.movie.pk}))
        self.assertEqual(response.status_code, 204)


class TestMoviesByTitle(TestCase):
    def test_request_client(self):
        response = self.client.get('/movies-by-title/')
        self.assertEqual(response.status_code, 200)

    def test_post_requests(self):
        response = self.client.post('/movies-by-title/', {'title': 'boat', 'year': '', 'type': 'movie'})
        self.assertEqual(response.status_code, 201)
        response = self.client.post('/movies-by-title/', {'title': 'asdasdas', 'year': '', 'type': 'movie'})
        self.assertEqual(response.status_code, 400)
        response = self.client.post('/movies-by-title/', {'title': 'boat', 'year': '', 'type': 'movie'})
        self.assertEqual(response.status_code, 400)
        response = self.client.post('/movies-by-title/', {'title': 'boat', 'year': '2001', 'type': 'movie'})
        self.assertEqual(response.status_code, 201)
        response = self.client.post('/movies-by-title/', {'title': 'boat', 'year': '2001', 'type': 'movie'})
        self.assertEqual(response.status_code, 400)
        response = self.client.post('/movies-by-title/', {'title': 'boat', 'year': '', 'type': 'series'})
        self.assertEqual(response.status_code, 201)
        response = self.client.post('/movies-by-title/', {'title': 'a', 'year': '', 'type': 'episode'})
        # don't know why, but OMDB doesn't find any of these
        self.assertEqual(response.status_code, 400)
        response = self.client.post('/movies-by-title/', {'title': 'a', 'year': '2004', 'type': 'series'})
        self.assertEqual(response.status_code, 201)
        response = self.client.post('/movies-by-title/', {'title': 'boat', 'year': '2004', 'type': 'episode'})
        # don't know why, but OMDB doesn't find any of these
        self.assertEqual(response.status_code, 400)
        response = self.client.post('/movies-by-title/', {'title': '', 'year': '2001', 'type': 'movie'})
        self.assertEqual(response.status_code, 400)
        response = self.client.post('/movies-by-title/', {'title': 'sky', 'year': 'asaa', 'type': 'movie'})
        # I know that it is strange but OMBD works that way
        self.assertEqual(response.status_code, 201)


class TestFavouritesMoviesByUser(TestCase):
    def setUp(self):
        self.username = 'testtest'
        self.password = 'password123'
        self.user = User.objects.create_user(self.username, self.password)

    def test_request_anonymous_user(self):
        response = self.client.get('/favourites-movies/')
        self.assertEqual(response.status_code, 403)

    def test_request_user(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/favourites-movies/')
        self.assertEqual(response.status_code, 200)

    def test_favourite_list(self):
        pass


class TestRateMovie(TestCase):
    def setUp(self):
        Movie.objects.create(title='abc')
        Movie.objects.create(title='def')
        Movie.objects.create(title='ghi')
        self.username = 'testtest'
        self.password = 'password123'
        self.user = User.objects.create_user(self.username, self.password)

    def test_request_anonymous_user(self):
        response = self.client.get('/rate/')
        self.assertEqual(response.status_code, 403)

    def test_request_user(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/rate/')
        self.assertEqual(response.status_code, 200)

    def test_rate_movie_post(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/rate/', {"rating": 4, "movie": 1})
        self.assertEqual(response.status_code, 201)
        response = self.client.post('/rate/', {"rating": 5, "movie": 1})
        self.assertEqual(response.status_code, 400)
        response = self.client.post('/rate/', {"rating": 7, "movie": 2})
        self.assertEqual(response.status_code, 201)
        response = self.client.post('/rate/', {"rating": -1, "movie": 3})
        self.assertEqual(response.status_code, 400)
        response = self.client.post('/rate/', {"rating": 11, "movie": 3})
        self.assertEqual(response.status_code, 400)
        response = self.client.post('/rate/', {"rating": 'asd', "movie": 3})
        self.assertEqual(response.status_code, 400)
        response = self.client.post('/rate/', {"rating": 4, "movie": 5})
        self.assertEqual(response.status_code, 400)
        self.client.logout()
        user_2 = User.objects.create_user(username='testtest2', password='abcderfgh')
        self.client.force_login(user=user_2)
        response = self.client.post('/rate/', {"rating": 4, "movie": 1})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(MovieRating.objects.filter(user=self.user).count(), 2)
        self.assertEqual(MovieRating.objects.filter(user=user_2).count(), 1)


class TestMovieRateDetail(TestCase):
    def setUp(self):
        movie_first = Movie.objects.create(title='abc')
        movie_second = Movie.objects.create(title='def')
        movie_third = Movie.objects.create(title='ghi')
        self.username = 'testtest'
        self.password = 'password123'
        self.user = User.objects.create_user(self.username, self.password)
        user_2 = User.objects.create_user(username='testtest2', password='12345678')
        MovieRating.objects.create(rating=8, movie=movie_first, user=self.user)
        MovieRating.objects.create(rating=7, movie=movie_second, user=self.user)
        MovieRating.objects.create(rating=1, movie=movie_third, user=user_2)

    def test_request_anonymous_user(self):
        response = self.client.get('/rate/1/')
        self.assertEqual(response.status_code, 200)
        response = self.client.put('/rate/1/', {"rating": 5, "movie": 1})
        self.assertEqual(response.status_code, 403)

    def test_request_user(self):
        self.client.force_login(user=self.user)
        response = self.client.put('/rate/1/', {"rating": '5', "movie": 1}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response = self.client.put('/rate/1/', {"rating": -1, "movie": 1}, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response = self.client.put('/rate/1/', {"rating": 11, "movie": 1}, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response = self.client.put('/rate/1/', {"rating": 'avd', "movie": 1}, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response = self.client.put('/rate/3/', {"rating": 5, "movie": 3}, content_type='application/json')
        self.assertEqual(response.status_code, 403)
        response = self.client.delete('/rate/2/')
        self.assertEqual(response.status_code, 204)
        response = self.client.delete('/rate/3/')
        self.assertEqual(response.status_code, 403)






