import os
from datetime import date
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
    ("Kevin Feige", "kevin_feige.jpg"),
    ("Joe Russo", "russo.jpg"),
    ("Stephen Mcfeely", "stephen_mcfeely.jpg"),
    ("Christopher Markus", "christopher_markus.jpg"),
    ("Robert Downey, Jr.", "robert-downey-jr.jpg"),
    ("Chris Evans", "chris.jpg"),
    ("Chris Hemsworth", "hemsworth.jpg"),
    ("Scarlett Johansson", "scarlett.jpeg"),
    ("Dave Bautista", "dave_bautista.jpg"),
    ("Adam Robitel","Adam Robitel.jpg"),
    ("Jason Blum","Jason Blum.jpg"),
    ("Lin Shaye","Lin Shaye.jpeg"),
    ("Leigh Whannell","Leigh Whannell.jpg"),
    ("Angus Sampson","Angus Sampson.jpg"),
    ("Spencer Locke","Spencer Locke.jpg"),
    
]

movies = [
    (
        "Joker",
        "joker.jpg",
        "In Gotham City, mentally troubled comedian Arthur Fleck is disregarded and mistreated by society. He then embarks on a downward spiral of revolution and bloody crime. This path brings him face-to-face with his alter-ego: the Joker.",
        "R",
        ["Crime", "Comic Books", "Drama", "Thriller"],
        date(2019, 10, 4),
        70000000,
        1074000000,
        ["Todd Phillips"],
        "Todd Phillips",
        ["Todd Phillips"],
        ["Joaquin Phoenix"],
        ["Robert De Niro"],
        ["joker_screen_1.png", "joker_screen_2.png"]
    ),
    (
        "Avengers Infinity War",
        "infinity.jpeg",
        "Iron Man, Thor, the Hulk and the rest of the Avengers unite to battle their most powerful enemy yet -- the evil Thanos. On a mission to collect all six Infinity Stones, Thanos plans to use the artifacts to inflict his twisted will on reality. The fate of the planet and existence itself has never been more uncertain as everything the Avengers have fought for has led up to this moment.",
        "R",
        ["Action", "Adventure", "Comic Books", "Science Fiction", "Superheroes"],
        date(2018, 4, 27),
        316000000,
        2048000000,
        ["Kevin Feige"],
        "Joe Russo",
        ["Stephen Mcfeely", "Christopher Markus"],
        ["Robert Downey, Jr.", "Chris Evans", "Chris Hemsworth", "Scarlett Johansson"],
        ["Dave Bautista"],
        ["infinity_screen_1.jpg", "infinity_screen_2.jpg"]
    ),
    (
        "Insidious The Last Key",
        "Insidious.jpg",
        "Parapsychologist Elise Rainier receives a disturbing call from a man who claims that his house is haunted. Even more disturbing is the address of the house, which is where Elise lived as a child.",
        "R",
        ["Horror","Mystery","Thriller"],
        date(2018, 2, 4),
        500000000,
        3000000000,
        ["Adam Robitel"],
        "Jason Blum",
        ["Lin Shaye", "Leigh Whannell"],
        ["Angus Sampson"],
        ["Spencer Locke"],
        ["Insidious_screen_1.jpeg", "Insidious_screen_2.jpg"]
    )
]
def insert_testing_data(apps, schema_editor):
    def get_genere(name):
        return Genere.objects.get(name=name)
    def get_person(name):
        return Person.objects.get(name=name)
    for genere in generes:
        Genere.objects.get_or_create(name=genere)
    for rating in ratings:
        Rating.objects.get_or_create(name=rating)
    for person in people:
        person_exists = Person.objects.filter(name=person[0]).exists()

        if not person_exists:
            person_object = Person(name=person[0])
            print(f"New person {person_object} correctly added to database.")
            portrait_dir = os.path.join(os.path.dirname(__file__), f"images/{person[1]}")
            print(f"Portrait: {portrait_dir}")
            person_object.portrait.save(person[1], File(open(portrait_dir, "rb")))
            person_object.save()

        else:
            print(f"Person {person[0]} already in database. Skipping...")

    for movie in movies:
        movie_exists = Movie.objects.filter(title=movie[0]).exists()

        if not movie_exists:
            movie_object= Movie(
                title=movie[0],
                summary=movie[2],
                rating=Rating.objects.get(name=movie[3]),
                release_date=movie[5],
                budget=movie[6],
                returns=movie[7],
                director=Person.objects.get(name=movie[9])
                )
            print(f"New movie {movie_object} correctly added to database.")
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

        else:
            print(f"Movie {movie[0]} already in database. Skipping...")
