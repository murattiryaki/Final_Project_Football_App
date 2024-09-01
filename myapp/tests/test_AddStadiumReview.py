from django.test import TestCase
from myapp.models import Venue, StadiumReview, User

class AddStadiumReviewTest(TestCase):
    def test_add_stadium_review(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        venue = Venue.objects.create(id=1, name='Test Venue', capacity=10000)
        review = StadiumReview.objects.create(
            venue=venue,
            user=user,
            review_text="Great place!",
            rating=5
        )
        self.assertEqual(StadiumReview.objects.count(), 1)
        self.assertEqual(review.review_text, "Great place!")
