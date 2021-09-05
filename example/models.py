from django.db import models

from simple_graphql.django import register_schema


@register_schema()
class Organization(models.Model):
    name = models.TextField()
    address = models.TextField()


@register_schema()
class Person(models.Model):
    first_name = models.TextField()
    last_name = models.TextField()
    email = models.TextField()
    secret = models.TextField()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
