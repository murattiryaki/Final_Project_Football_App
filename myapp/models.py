from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class FavoriteTeam(models.Model):
    id = models.BigAutoField(primary_key=True)
    team_name = models.CharField(max_length=255)
    team_id = models.IntegerField(default=0)  # Assuming team_id is coming from the API
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.team_name

class UserFavoriteTeam(models.Model):
    team = models.ForeignKey('Team', on_delete=models.CASCADE)  # Foreign key to the Team model
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_teams')

    class Meta:
        unique_together = ('user', 'team')

    def __str__(self):
        return f"{self.user.username} - {self.team.name}"

class UserReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} on {self.team.name}"
