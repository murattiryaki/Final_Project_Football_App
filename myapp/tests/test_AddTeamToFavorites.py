from django.test import TestCase
from myapp.models import Team, UserFavoriteTeam, User

class AddTeamToFavoritesTest(TestCase):
    def test_add_team_to_favorites(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        team = Team.objects.create(id=1, name='Test Team')
        favorite = UserFavoriteTeam.objects.create(user=user, team=team)
        self.assertEqual(UserFavoriteTeam.objects.count(), 1)
        self.assertEqual(favorite.team.name, "Test Team")
