from django.db import models
from datetime import timedelta
from django.utils.timezone import localdate, localtime
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse_lazy

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
    # RELATED URLS
    @property # Details page
    def details_page_url(self):
        return reverse_lazy("movies:movie_detail", kwargs = {"pk": self.pk})
    @property # Create a review of this movie
    def create_review_url(self):
        return reverse_lazy(
            "movies:review_create", kwargs = {"movie_pk": self.pk}
            )
    class Meta:
        ordering = ["-release_date"]
    def __str__(self):
        return f"{self.title} ({self.release_date.year})"

class MovieScreenshot(MetaData):
    movie = models.ForeignKey(
            Movie, on_delete=models.CASCADE,
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
    class Meta:
        # Single like per item per user!
        unique_together = ["content_type", "object_id", "create_user"]
    def __str__(self):
        return f"A like from {self.create_user.username} " \
                f"on {self.content_type} #{self.object_id}"

def find_original_post(comment):
    if comment.content_type == ContentType.objects.get_for_model(Review):
        return comment.content_object
    else:
        return find_original_post(comment.content_object)

class Comment(MetaData):
    body = models.TextField(max_length=128)
    likes = GenericRelation(Like)
    @property
    def like_count(self):
        return self.likes.count()
    responses = GenericRelation("Comment")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    # RELATED URLS
    @property # Find the original review
    def original_post(self):
        return find_original_post(self)
    @property # Toggle like/unlike on comment
    def like_url(self):
        return reverse_lazy("movies:comment_like", kwargs = {"pk": self.pk})
    @property # Respond to comment
    def respond_url(self):
        return reverse_lazy(
            "movies:comment_respond",
            kwargs = {
                "movie_pk": self.original_post.movie.pk,
                "review_pk": self.original_post.pk,
                "comment_pk": self.pk
                }
            )
    @property # Delete a comment
    def delete_url(self):
        return reverse_lazy(
            "movies:comment_delete",
            kwargs = {
                "movie_pk": self.original_post.movie.pk,
                "review_pk": self.original_post.pk,
                "pk": self.pk
                }
            )
    def __str__(self):
        return f"Response #{self.pk} to {self.content_type} #{self.object_id}"

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
    likes = GenericRelation(Like)
    @property
    def like_count(self):
        return self.likes.count()
    comments = GenericRelation(Comment)
    # RELATED URLS
    @property # Movie details page
    def movie_detail_page_url(self):
        return reverse_lazy(
            "movies:movie_detail", kwargs = {"pk": self.movie.pk}
            )
    @property # Movie details page focused on this review
    def movie_detail_page_focused_url(self):
        return reverse_lazy(
            "movies:movie_detail", kwargs = {"pk": self.movie.pk}
            ) + f"#review{self.pk}"
    @property # Review details page
    def review_detail_page_url(self):
        return reverse_lazy(
            "movies:review_detail",
            kwargs = {"movie_pk": self.movie.pk, "pk": self.pk}
            )
    @property # Toggle like/unlike on review
    def like_url(self):
        return reverse_lazy("movies:review_like", kwargs = {"pk": self.pk})
    @property # Respond to review
    def respond_url(self):
        return reverse_lazy(
            "movies:review_respond",
            kwargs = {"movie_pk": self.movie.pk, "review_pk": self.pk}
            )
    @property # Delete review
    def delete_url(self):
        return reverse_lazy(
            "movies:review_delete",
            kwargs = {"pk": self.pk, "movie_pk": self.movie.pk}
            )
    class Meta:
        # Only one review per movie per user!
        unique_together = ["create_user", "movie"]
        # Order by most recent
        ordering = ["-create_time"]
    def __str__(self):
        return f"Review #{self.pk} of {self.movie}"
