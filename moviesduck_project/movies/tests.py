from django.test import TestCase
from django.contrib.auth.models import User
from .models import Movie, Review, Comment

class UserTestCase(TestCase):
  def setUp(self):
    movie = Movie.objects.first()
    Review.objects.create(
      movie=movie,
      summary="lorem",
      body="lorem ipsum",
      score=10
    )
    User.objects.create(
      username="luismanuelglz",
      first_name="Luis",
      last_name="Glz",
      email="luis@mail.com",
      password="password123"
    )

  """
  Checks if the review is created properly.
  """
  def test_is_review_created_properly(self):
    movie = Movie.objects.first()
    review_exists = Review.objects.filter(movie=movie).exists()
    self.assertTrue(review_exists)

  """
  Checks if the review is deleted after the movie is deleted.
  """
  def test_is_review_deleted_after_delete_movie(self):
    movie = Movie.objects.first()
    movie.delete()
    review_exists = Review.objects.filter(movie=movie).exists()
    self.assertFalse(review_exists)
