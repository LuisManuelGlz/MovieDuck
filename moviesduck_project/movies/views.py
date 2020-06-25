from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.db.models import Prefetch
from .models import Movie, Review, Comment, Like
from datetime import timedelta
from django.urls import reverse_lazy
from django.utils.timezone import localtime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse

########## MOVIE LISTS ##########
class MovieListMixin(ListView):
    context_object_name = "movies"

class ReviewListMixin(ListView):
    context_object_name = "reviews"

##### HTML CAROUSEL-BASED LISTS #####
# New releases
class CarouselNewReleases(MovieListMixin):
    template_name = "movies/carousel_movie_list.html"
    queryset = Movie.objects.all()[:5]

# Trending
class CarouselTrending(MovieListMixin):
    template_name = "movies/carousel_movie_list.html"
    trending_list = True

    # Get movies BUT prefetch only reviews made in the last 24 hours
    queryset = Movie.objects \
            .prefetch_related(Prefetch("reviews", \
            Review.objects.filter(create_time__gt = localtime() - \
            timedelta(days=1)))) \
            .order_by("reviews__count")[:10]

# Most recent reviews
class CarouselRecentReviews(ReviewListMixin):
    template_name = "movies/carousel_review_list.html"
    queryset = Review.objects.all()[:10]

########## MOVIE DETAILS ##########
class MovieDetails(DetailView):
    model = Movie

########## REVIEWS, COMMENTS, & LIKES ##########
### Reviews
class ReviewMixin(LoginRequiredMixin):
    model = Review
    #context_object_name = "review"

# Create a review for a movie
class CreateReview(ReviewMixin, CreateView):
    http_method_names = ["post"]

    # Return to movie details page and jump to review just created
    def get_success_url(self):
        return reverse_lazy(
            "movie_details",
            kwargs = {"pk": self.object.movie.pk, "review_pk": self.object.pk}
            )

    # Add user and movie from URL arguments
    def form_valid(self, form):
        form.instance.create_user = self.request.user
        form.instance.movie = Movie.objects.get(pk=self.kwargs["movie_pk"])
        return super.form_valid(form)

# Delete a review
class DeleteReview(ReviewMixin, DeleteView):
    # Return to movie details page
    def get_success_url(self):
        return reverse_lazy(
            "movie_details",
            kwargs = {"pk": self.object.movie.pk}
            )

# Toggle like/dislike on a review
@login_required
def toggle_like_review(request, pk):
    like, like_is_new = Like.objects.get_or_create(
        create_user = request.user,
        content_type = ContentType.objects.get_for_model(Review),
        object_id = pk
        )
    if not like_is_new: like.delete()
    return HttpResponse("Liked!" if like_is_new else "Unliked!")

### Comments

# Toggle like/dislike on a comment
@login_required
def toggle_like_comment(request, pk):
    like, like_is_new = Like.objects.get_or_create(
        create_user = request.user,
        content_type = ContentType.objects.get_for_model(Comment),
        object_id = pk
        )
    if not like_is_new: like.delete()
    return HttpResponse("Liked!" if like_is_new else "Unliked!")
