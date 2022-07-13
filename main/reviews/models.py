from django.db import models
from django.contrib.auth.models import User


class GrowKit(models.Model):
    name = models.CharField(max_length=125)
    url = models.TextField()

    def __str__(self):
        return self.name


class MushroomTypes(models.Model):
    name = models.CharField(max_length=125)

    def __str__(self):
        return self.name


class Variety(models.Model):
    name = models.CharField(max_length=125)
    content = models.TextField()
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.name


class VarietySite(models.Model):
    name = models.CharField(max_length=125)
    variety = models.ForeignKey(
        Variety,
        on_delete=models.CASCADE,
        related_name="sites",
        related_query_name="site",
    )
    growkit = models.ForeignKey(
        GrowKit,
        on_delete=models.CASCADE,
        related_name="sites",
        related_query_name="site",
    )
    url = models.TextField()
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    title = models.CharField(max_length=125)
    content = models.TextField()
    variety = models.ForeignKey(
        Variety,
        on_delete=models.CASCADE,
        related_name="comments",
        related_query_name="comment",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        related_query_name="comment",
    )
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.title
