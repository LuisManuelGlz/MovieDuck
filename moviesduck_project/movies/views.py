from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.db.models import Prefetch
from .models import Movie, Review, Comment, Like
from .forms import ReviewForm, CommentForm
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

########## MOVIE LIST ##########
class MovieList(LoginRequiredMixin, ListView):
    model = Movie
    context_object_name = "movies"

########## MOVIE DETAILS ##########
class MovieDetail(LoginRequiredMixin, DetailView):
    model = Movie
    review_form = ReviewForm
    template_name = "movies/movie_detail.html"

########## REVIEWS, COMMENTS, & LIKES ##########
class ReviewMixin(LoginRequiredMixin):
    model = Review
    #context_object_name = "review"

class CommentMixin(LoginRequiredMixin):
    model = Comment

### Reviews
# Review detail
class ReviewDetail(DetailView):
    model = Review
    template_name = "movies/review_detail.html"
    comment_form = CommentForm

# Create a review for a movie
class CreateReview(ReviewMixin, CreateView):
    http_method_names = ["post"]
    form_class = ReviewForm

    # Return to movie details page and jump to review just created
    def get_success_url(self):
        return reverse_lazy(
            "movies:movie_detail", kwargs = {"pk": self.object.movie.pk}
            ) + f"#review{self.object.pk}"

    # Add user and movie from URL arguments
    def form_valid(self, form):
        form.instance.create_user = self.request.user
        form.instance.movie = Movie.objects.get(pk=self.kwargs["movie_pk"])
        return super().form_valid(form)

# Delete a review
class DeleteReview(ReviewMixin, DeleteView):
    http_method_names = ["post"]

    # Return to movie details page
    def get_success_url(self):
        return reverse_lazy(
            "movies:movie_detail",
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
    return HttpResponse(f"like-review{pk}")

# Respond to a review
class RespondToReview(CommentMixin, CreateView):
    http_method_names = ["post"]
    form_class = CommentForm

    # Reload review details page focused on just made comment
    def get_success_url(self):
        return reverse_lazy(
            "movies:review_detail",
            kwargs = {
                "movie_pk": self.kwargs["movie_pk"],
                "pk": self.kwargs["review_pk"]
                }
            ) + f"#comment{self.object.pk}"

    # Add user and review from URL arguments
    def form_valid(self, form):
        form.instance.create_user = self.request.user
        form.instance.content_type = ContentType.objects.get_for_model(Review)
        form.instance.object_id = self.kwargs["review_pk"]
        return super().form_valid(form)

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
    return HttpResponse(f"like-comment{pk}")

# Delete a comment
class DeleteComment(CommentMixin, DeleteView):
    http_method_names = ["post"]

    # Return to review details page
    def get_success_url(self):
        return reverse_lazy(
            "movies:review_detail",
            kwargs = {
                "movie_pk": self.kwargs["movie_pk"],
                "pk": self.kwargs["review_pk"]
                }
            )

# Respond to a comment
class RespondToComment(CommentMixin, CreateView):
    http_method_names = ["post"]
    form_class = CommentForm

    # Reload review details page focused on just made comment
    def get_success_url(self):
        return reverse_lazy(
            "movies:review_detail",
            kwargs = {
                "movie_pk": self.kwargs["movie_pk"],
                "pk": self.kwargs["review_pk"]
                }
            ) + f"#comment{self.object.pk}"

    # Add user and parent comment from URL arguments
    def form_valid(self, form):
        form.instance.create_user = self.request.user
        form.instance.content_type = ContentType.objects.get_for_model(Comment)
        form.instance.object_id = self.kwargs["comment_pk"]
        return super().form_valid(form)
