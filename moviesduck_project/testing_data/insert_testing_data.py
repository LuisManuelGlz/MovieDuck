import os
from movies.models import *
from django.core.files import File
from django.contrib.auth.models import User

generes = [
    "Action",
    "Adventure",
    "Animated",
    "Biography",
    "Crime",
    "Comedy",
    "Comic Books",
    "Drama",
    "Family",
    "Fantasy",
    "History",
    "Horror",
    "Musical",
    "Mystery",
    "Science Fiction",
    "Superheroes",
    "Thriller",
    "War",
    "Western"
]

ratings = [
    "NR"
    "G",
    "PG",
    "PG-13",
    "R",
    "NC-17",
    "NR"
]

people = [
    ("Todd Phillips", "todd.jpg"),
    ("Joaquin Phoenix", "joaquin.jpg"),
    ("Robert De Niro", "robert.jpg"),
]

movies = [
    (
        "Joker",
        "joker.jpg",
        "In Gotham City, mentally troubled comedian Arthur Fleck is disregarded and mistreated by society. He then embarks on a downward spiral of revolution and bloody crime. This path brings him face-to-face with his alter-ego: the Joker.",
        "R",
        ["Crime", "Comic Books", "Drama", "Thriller"],
        "2019-10-04",
        70000000,
        1074000000,
        ["Todd Phillips"],
        "Todd Phillips",
        ["Todd Phillips"],
        ["Joaquin Phoenix"],
        ["Robert De Niro"],
        ["joker_screen_1.png", "joker_screen_2.png"]
    )
]
def insert_testing_data():
    def get_genere(name):
        return Genere.objects.get(name=name)
    def get_person(name):
        return Person.objects.get(name=name)
    for genere in generes:
        Genere.objects.get_or_create(name=genere)
    for rating in ratings:
        Rating.objects.get_or_create(name=rating)
    Movie.objects.all().delete()
    Person.objects.all().delete()
    for person in people:
        object = Person(name=person[0])
        portrait_dir = os.path.join(os.path.dirname(__file__), f"images/{person[1]}")
        print(f"Portrait: {portrait_dir}")
        object.portrait.save(person[1], File(open(portrait_dir, "rb")))
        object.save()
    for movie in movies:
        movie_object = Movie(
            title=movie[0],
            summary=movie[2],
            rating=Rating.objects.get(name=movie[3]),
            release_date=movie[5],
            budget=movie[6],
            returns=movie[7],
            director=Person.objects.get(name=movie[9])
        )
        poster_dir = os.path.join(os.path.dirname(__file__), f"images/{movie[1]}")
        print(f"Poster: {poster_dir}")
        movie_object.poster.save(movie[1], File(open(poster_dir, "rb")))
        movie_object.generes.add(*list(map(get_genere, movie[4])))
        movie_object.producers.add(*list(map(get_person, movie[8])))
        movie_object.writers.add(*list(map(get_person, movie[10])))
        movie_object.stars.add(*list(map(get_person, movie[11])))
        movie_object.cast.add(*list(map(get_person, movie[12])))
        movie_object.save()
        for screenshot in movie[13]:
            screenshot_object = MovieScreenshot(movie=movie_object)
            screenshot_dir = os.path.join(os.path.dirname(__file__), f"images/{screenshot}")
            print(f"Screenshot: {screenshot_dir}")
            screenshot_object.image.save(screenshot, File(open(screenshot_dir, "rb")))
            screenshot_object.save()
