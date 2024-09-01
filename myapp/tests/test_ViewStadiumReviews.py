from django.test import TestCase
from django.urls import reverse
from myapp.models import Venue, User, StadiumReview

class ViewStadiumReviewsTest(TestCase):
    def setUp(self):
        # Create test user and log them in
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Create test venue
        self.venue = Venue.objects.create(
            name='Test Venue',
            address='Test Address',
            city='Test City',
            capacity=10000
        )

    def test_view_stadium_reviews(self):
        # Create a review for the venue
        StadiumReview.objects.create(
            venue=self.venue,
            user=self.user,
            review_text="Great stadium!",
            rating=5
        )

        # Test the review page
        response = self.client.get(reverse('venue_detail', args=[self.venue.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Great stadium!")
