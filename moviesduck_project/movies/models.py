from django.db import models
from datetime import timedelta
from django.utils.timezone import localdate, localtime
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

########## REGISTER METADATA ##########
class MetaData(models.Model):
    create_user = models.ForeignKey(
            User, null=True,
            on_delete=models.SET_NULL,
            related_name="created_%(class)s"
            )
    create_time = models.DateTimeField(auto_now_add=True)
    update_user = models.ForeignKey(
            User, null=True,
            on_delete=models.SET_NULL,
            related_name="updated_%(class)s"
            )
    update_time = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

########## MOVIE ATTRIBUTES ##########
class GenericAttribute(MetaData):
    name = models.CharField(max_length=256, unique=True)
    def __str__(self):
        return self.name
    class Meta:
        abstract = True

class Genere(GenericAttribute):
    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(*args, **kwargs)

class Rating(GenericAttribute):
    pass

########## PEOPLE ##########
class Person(MetaData):
    name = models.CharField(max_length=256, unique=True)
    portrait = models.ImageField(
            upload_to="portraits/",
            null=True, blank=True
            )
    class Meta:
        verbose_name_plural = "People"
    def __str__(self):
        return self.name

########## MOVIES ##########
class Movie(MetaData):
    # GENERAL INFO
    title = models.CharField(max_length=256)
    poster = models.ImageField(upload_to="posters/")
    summary = models.TextField()
    rating = models.ForeignKey(Rating, on_delete=models.PROTECT)
    generes = models.ManyToManyField(Genere, related_name="genre_movies")
    # RELEASE INFO
    release_date = models.DateField()
    budget = models.DecimalField(max_digits=14, decimal_places=2)
    returns = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    # MEMBERS
    producers = models.ManyToManyField(
            Person, blank=True,
            related_name="movies_produced"
            )
    director = models.ForeignKey(
            Person, null=True, blank=True,
            on_delete=models.PROTECT,
            related_name="movies_directed")
    writers = models.ManyToManyField(
            Person, blank=True,
            related_name="movies_written"
            )
    stars = models.ManyToManyField(
            Person, blank=True,
            related_name="movies_starred"
            )
    cast = models.ManyToManyField(
            Person, blank=True,
            related_name="movies_appeared"
            )
    class Meta:
        ordering = ["-release_date"]
    def __str__(self):
        return f"{self.title} ({self.release_date.year})"

class MovieScreenshot(MetaData):
    movie = models.ForeignKey(
            Movie,
            on_delete=models.CASCADE,
            related_name="screenshots"
            )
    image = models.ImageField(upload_to="screenshots/")
    def __str__(self):
        return f"A screenshot of {self.movie}"

########## REVIEWS, COMMENTS, & LIKES ##########
class Like(MetaData):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    def __str__(self):
        return f"A like from {self.create_user.username} " \
                f"on {self.content_type} #{self.object_id}"

class Comment(MetaData):
    body = models.TextField(max_length=128)
    likes = GenericRelation(
            Like,
            related_query_name="liked_item"
            )
    responses = GenericRelation(
            "Comment",
            related_query_name="parent_item"
            )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    def __str__(self):
        return f"A response to {self.content_type} #{self.object_id}"

class Review(MetaData):
    movie = models.ForeignKey(
            Movie,
            on_delete=models.CASCADE,
            related_name="reviews"
            )
    score = models.PositiveSmallIntegerField(
            validators=[MinValueValidator(0), MaxValueValidator(10)]
            )
    summary = models.TextField(max_length=128)
    body = models.TextField()
    likes = GenericRelation(
            Like,
            related_query_name="liked_item"
            )
    @property
    def like_count(self):
        return self.likes.count()
    comments = GenericRelation(
            Comment,
            related_query_name="parent_item"
            )
    class Meta:
        ordering = ["-create_time"]
    def __str__(self):
        return f"A review of {self.movie}"
