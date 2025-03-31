from django.urls import path


from .views import(
    UserRegistration_view,
    get_summaries_view,
    get_places_recommendation_view,
    get_best_nearby_places_to_visit_view,
)

urlpatterns = [
    path('register/user', UserRegistration_view.as_view(), name='userRegistration'),
    path('sums', get_summaries_view, name='sums'),
    path('recommend', get_places_recommendation_view, name="recommend"),
    path('nearby', get_best_nearby_places_to_visit_view, name="nearby"),
]
