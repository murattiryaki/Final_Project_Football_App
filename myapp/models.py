from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=200)

class Stadium(models.Model):
    name = models.CharField(max_length=200)

class Fixture(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)
