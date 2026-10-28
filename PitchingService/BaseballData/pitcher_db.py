from django.db import models

class PitchingStats(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    player_id = models.IntegerField(default=0)
    pitch_type = models.CharField(max_length=200,null=True, blank=True)
    velocity = models.FloatField(null=True, blank=True)
    spin = models.FloatField(null=True, blank=True)
    location = models.JSONField(default=list)
    zone = models.JSONField(default=list)

class Pitcher(models.Model):
    def __str__(self):
        return self.name

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200, db_index=True)
    position = models.CharField(max_length=2,null=True, blank=True)
    jersey_number = models.IntegerField(null=True, blank=True)
    team = models.CharField(max_length=200,null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    birthplace = models.CharField(max_length=200,null=True, blank=True)
    handedness = models.CharField(max_length=1,null=True, blank=True)
