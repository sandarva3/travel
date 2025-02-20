from django.urls import path


from .views import(
    UserRegistration_view,
)

urlpatterns = [
    path('register/user', UserRegistration_view.as_view(), name='userRegistration'),
]
