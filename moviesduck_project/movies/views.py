from django.views.generic import ListView, DetailView
from django.db.models import Prefetch
from .models import Movie, Review
from datetime import timedelta
from django.utils.timezone import localtime

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
