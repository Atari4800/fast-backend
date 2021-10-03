from django.db import models


class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    modified_on = models.DateTimeField(auto_now=True, editable=False)
