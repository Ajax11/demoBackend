from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return f"{self.title}"
