from django import template
register = template.Library()

########## CUSTOM FILTERS ##########
@register.filter(name="liked_by") # Check if the user has liked this post
def item_liked_by_user(item, user):
    return item.likes.filter(create_user = user).exists()
