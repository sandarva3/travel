from django.urls import path


from .views import(
    UserRegistration_view,
    get_summaries_view,
    get_all_places_view,
    get_places_recommendation_view,
)

urlpatterns = [
    path('register/user', UserRegistration_view.as_view(), name='userRegistration'),
    path('sums', get_summaries_view, name='sums'),
    path('allPlaces', get_all_places_view, name="all_places"),
    path('recommend', get_places_recommendation_view, name="recommend")
]
