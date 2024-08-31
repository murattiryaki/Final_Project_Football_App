from django.contrib import admin
from .models import StadiumReview

@admin.register(StadiumReview)
class StadiumReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'venue', 'rating', 'date_added')
    search_fields = ('user__username', 'venue__name')
    list_filter = ('rating', 'date_added')
