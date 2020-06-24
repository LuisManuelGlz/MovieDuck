from django.urls import path
from movies import views

app_name = "movies"
urlpatterns = [
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
    ##########
    path( # Toggle like/unlike on a review
        "reviews/<int:pk>/like",
        views.toggle_like_review,
        name="review_like"
        ),
    ##########
    # Comment interaction
    path( # Toggle like/unlike on a comment
        "comments/<int:pk>/like",
        views.toggle_like_comment,
        name="comment_like"
        ),
]

"""
# Movie details page
path( # Normal movie details page
    "<int:pk>",
    views.MovieDetails.as_view(),
    name="movie_details"
    ),
path( # Movie details page focused on user's just created review
    "<int:pk>#review<int:review_pk>",
    views.MovieDetails.as_view(),
    name="movie_details"
    ),
# Review interaction
path( # Create a review
    "reviews/create/for_<int:movie_pk>",
    views.CreateReview.as_view(),
    name="review_create"
    ),
path( # Delete a review
    "reviews/<int:pk>/delete",
    views.DeleteReview.as_view(),
    name="review_delete"
    ),
path( # Toggle like/unlike on a review
    "reviews/<int:review>/like",
    views.toggle_like_review,
    name="review_like"
    ),
path( # Respond to a review
    "reviews/<int:pk>/respond",
    views.RespondToReview.as_view(),
    name="respond"
    ),

path( # Respond to a comment
    "comments/<int:comment_pk>/respond"
    ),
"""
