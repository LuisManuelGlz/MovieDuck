from django.urls import path
from movies import views
from django.views.generic import TemplateView # temporal import

app_name = "movies"
urlpatterns = [
    path("rev-detail/", TemplateView.as_view(template_name="movies/review_detail.html"), name="review_detail"),
    # Carousel-based lists
    path( # Newest movies
        "newest/carousel/",
        views.CarouselNewReleases.as_view(),
        name="newest_carousel"
        ),
    path( # Trending (most reviews in last 24 hours)
        "trending/carousel/",
        views.CarouselTrending.as_view(),
        name="trending_carousel"
        ),
    path( # Newest reviews
        "newreviews/carousel/",
        views.CarouselRecentReviews.as_view(),
        name="newreviews_carousel"
        ),
    # Movie details page
    path( # Normal movie details page
        "<int:pk>",
        views.MovieDetail.as_view(),
        name="movie_detail"
        ),
    # Review interaction
    path( # Create a review
        "<int:movie_pk>/reviews/create",
        views.CreateReview.as_view(),
        name="review_create"
        ),
    path( # Delete a review
        "<int:movie_pk>/reviews/<int:pk>/delete",
        views.DeleteReview.as_view(),
        name="review_delete"
        ),
    path( # Toggle like/unlike on a review
        "reviews/<int:pk>/like",
        views.toggle_like_review,
        name="review_like"
        ),
    path( # Respond to a review
        "<int:movie_pk>/reviews/<int:review_pk>/respond",
        views.RespondToReview.as_view(),
        name="review_respond"
        ),
    # Comment interaction
    path( # Toggle like/unlike on a comment
        "comments/<int:pk>/like",
        views.toggle_like_comment,
        name="comment_like"
        ),
    path( # Delete a comment
            "<int:movie_pk>/comments/<int:pk>/delete",
            views.DeleteComment.as_view(),
            name="comment_delete"
        ),
    path( # Respond to a comment
        "<int:movie_pk>/comments/<int:comment_pk>/respond",
        views.RespondToComment.as_view(),
        name="comment_respond"
        ),
]
