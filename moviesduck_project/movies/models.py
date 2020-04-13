from django.db import models
from django.contrib.auth.models import User

########## REGISTER METADATA ##########
class MetaData(models.Model):
    create_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="created_%(class)s")
    create_time = models.DateTimeField(auto_now_add=True)
    update_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="updated_%(class)s")
    update_time = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

########## MOVIE ATTRIBUTES ##########
class GenericAttribute(MetaData):
    name = models.CharField(max_length=256, unique=True)
    description = models.TextField()
    def __str__(self):
        return f"{self.name}"
    def save(self):
        self.name = self.name.title()
    class Meta:
        abstract = True

class Genere(GenericAttribute):
    pass

class SubGenere(GenericAttribute):
    parent = models.ForeignKey(Genere, on_delete=models.PROTECT, related_name="subgeneres")
    def __str__(self):
        return f"{self.parent.name} - {self.name}"

class Rating(GenericAttribute):
    pass

########## PEOPLE ##########
class Person(MetaData):
    name = models.CharField(max_length=256)
    portrait = models.ImageField(upload_to="portraits/")
    birth_date = models.DateField()
    class Meta:
        verbose_name_plural = "People"

########## MOVIES ##########
class Movie(MetaData):
    # GENERAL INFO
    title = models.CharField(max_length=256)
    poster = models.ImageField(upload_to="posters/")
    rating = models.ForeignKey(Rating, on_delete=models.PROTECT)
    generes = models.ManyToManyField(Genere, related_name="genre_movies")
    subgeneres = models.ManyToManyField(Genere, related_name="subgenere_movies")
    # RELEASE INFO
    release_date = models.DateField()
    budget = models.DecimalField(max_digits=14, decimal_places=2)
    returns = models.DecimalField(max_digits=14, decimal_places=2)
    # MEMBERS
    producer = models.ManyToManyField(Person, related_name="movies_produced")
    director = models.ForeignKey(Person, on_delete=models.PROTECT, related_name="movies_directed")
    writers = models.ManyToManyField(Person, related_name="movies_written")
    stars = models.ManyToManyField(Person, related_name="movies_starred")
    cast = models.ManyToManyField(Person, related_name="movies_appeared")
    def __str__(self):
        return f"{self.title} ({self.release_date.year})"
