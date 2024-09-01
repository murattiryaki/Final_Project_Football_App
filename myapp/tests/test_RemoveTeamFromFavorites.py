from django.test import TestCase
from myapp.models import Team, UserFavoriteTeam, User

class RemoveTeamFromFavoritesTest(TestCase):
    def test_remove_team_from_favorites(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        team = Team.objects.create(id=1, name='Test Team')
        favorite = UserFavoriteTeam.objects.create(user=user, team=team)
        favorite.delete()
        self.assertEqual(UserFavoriteTeam.objects.count(), 0)
