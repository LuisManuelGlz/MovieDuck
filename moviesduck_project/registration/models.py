from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

def custom_upload_to(instance, filename):
  old_instance = Profile.objects.get(pk=instance.pk)
  if old_instance.avatar != 'default.jpg':
    old_instance.avatar.delete()
  return f'profiles_pics/{old_instance.user.username}/{filename}'

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  avatar = models.ImageField(default='default.jpg', upload_to=custom_upload_to)
  location = models.CharField(max_length=256, default="", blank=True, null=True)
  bio = models.TextField(default="", blank=True, null=True)

  def __str__(self):
    return f"{self.user.username} profile"

@receiver(post_save, sender=User)
def ensure_profile_exists(sender, instance, **kwargs):
    if kwargs.get('created', False): # si la instancia es falsa, es decir, que no se ha creado
        Profile.objects.get_or_create(user=instance) # enlazamos
