from django.urls import path
from movies import views

app_name = "movies"
urlpatterns = [
    # Carousel-based lists
    path("newest/carousel/", views.CarouselNewReleases.as_view(), name="newest_carousel"),
    path("trending/carousel/", views.CarouselTrending.as_view(), name="trending_carousel"),
    path("newreviews/carousel/", views.CarouselRecentReviews.as_view(), name="newreviews_carousel"),
]
