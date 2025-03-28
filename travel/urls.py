from django.urls import path


from .views import(
    UserRegistration_view,
    get_summaries_view,
)

urlpatterns = [
    path('register/user', UserRegistration_view.as_view(), name='userRegistration'),
    path('sums', get_summaries_view, name='sums'),
]
