from django.db import models

class PlaylistSimilarity(models.Model):
    playlist1 = models.CharField(max_length=255)
    playlist2 = models.CharField(max_length=255)
    similarity = models.FloatField()
