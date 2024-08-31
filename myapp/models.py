from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class UserFavoriteTeam(models.Model):
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_teams')

    class Meta:
        unique_together = ('user', 'team')

    def __str__(self):
        return f"{self.user.username} - {self.team.name}"

from django.db import models
from django.contrib.auth.models import User

class Venue(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    capacity = models.IntegerField()
    image = models.URLField(blank=True)

    def __str__(self):
        return self.name

class StadiumReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} on {self.venue.name}"


