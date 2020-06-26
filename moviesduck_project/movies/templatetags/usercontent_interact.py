from django import template
register = template.Library()

########## CUSTOM FILTERS ##########
# Check if the user has liked this post
@register.filter(name="liked_by")
def item_liked_by_user(item, user):
    return item.likes.filter(create_user = user).exists()

# Check if user has already reviewed this
@register.filter(name="already_reviewed_by")
def movie_reviewed_by_user(movie, user):
	return movie.reviews.filter(create_user = user).exists()
