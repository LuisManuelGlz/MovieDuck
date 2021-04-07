from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile
import re

class UserTestCase(TestCase):
  def setUp(self):
    User.objects.create(
      username="luismanuelglz",
      first_name="Luis",
      last_name="Glz",
      email="luis@mail.com",
      password="password123"
    );

  """
  Checks if the sign up page loads successful.
  """
  def test_sign_up_loads_properly(self):
    response = self.client.get('/accounts/signup/')
    self.assertEqual(response.status_code, 200)

  """
  Checks if the sign up page uses the correct template.
  """
  def test_sign_up_correct_template(self):
    response = self.client.get('/accounts/signup/')
    self.assertTemplateUsed(response, 'registration/signup.html')

  """
  Checks if the profile is created after the user is created.
  """
  def test_is_profile_created(self):
    user = User.objects.get(username="luismanuelglz")
    profile_exists = Profile.objects.filter(user=user).exists()
    self.assertTrue(profile_exists)

  """
  Checks if the avatar is a JPG file.
  """
  def test_is_avatar_image_jpg(self):
    user = User.objects.get(username="luismanuelglz")
    profile = Profile.objects.get(user=user)
    result = re.search(".jpg", str(profile.avatar))
    self.assertTrue(result)

  """
  Checks if th avatar is not a PNG file.
  """
  def test_avatar_image_is_not_jpg(self):
    user = User.objects.get(username="luismanuelglz")
    profile = Profile.objects.get(user=user)
    result = re.search(".png", str(profile.avatar))
    self.assertFalse(result)

  """
  Checks if the profile is deleted after the user is deleted.
  """
  def test_is_profile_deleted_after_delete_user(self):
    user = User.objects.get(username="luismanuelglz")
    user.delete()
    profile_exists = Profile.objects.filter(user=user).exists()
    self.assertFalse(profile_exists)
    
