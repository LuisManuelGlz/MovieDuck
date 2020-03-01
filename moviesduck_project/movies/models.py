from django.db import models
from django.contrib.auth.models import User

########## REGISTER METADATA ##########
class MetaData(models.Model):
    create_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="created_%(class)s")
    create_time = models.DateTimeField(auto_now_add=True)
    update_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="updated_%(class)s")
    update_time = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

########## MOVIE ATTRIBUTES ##########
class GenericAttribute(MetaData):
    name = models.CharField(max_length=256, unique=True)
    description = models.TextField()
    def __str__(self):
        return f"{self.name}"
    def save(self):
        self.name = self.name.title()
    class Meta:
        abstract = True

class Genere(GenericAttribute):
    pass

class SubGenere(GenericAttribute):
    parent = models.ForeignKey(Genere, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.parent.name} - {self.name}"

class Rating(GenericAttribute):
    pass

########## PEOPLE ##########
class Person(MetaData):
    name = models.CharField(max_length=256, unique=True)
    birth_date = models.DateField()
    # INCOMPLETO
