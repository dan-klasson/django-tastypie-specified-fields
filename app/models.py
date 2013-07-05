from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=30)

class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.ForeignKey(Country)
    website = models.URLField()

class Language(models.Model):
    name = models.CharField(max_length=30)

class Author(models.Model):
    language = models.ForeignKey(Language)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher)
    publication_date = models.DateField()


