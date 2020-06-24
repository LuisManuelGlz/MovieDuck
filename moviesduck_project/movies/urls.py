from django.urls import path
from movies import views
from django.views.generic import TemplateView # temporal import

app_name = "movies"
urlpatterns = [
    path("detail/", TemplateView.as_view(template_name="movies/movie_detail.html"), name="movie_detail"),
    # Carousel-based lists
    path("newest/carousel/", views.CarouselNewReleases.as_view(), name="newest_carousel"),
    path("trending/carousel/", views.CarouselTrending.as_view(), name="trending_carousel"),
    path("newreviews/carousel/", views.CarouselRecentReviews.as_view(), name="newreviews_carousel"),
]
