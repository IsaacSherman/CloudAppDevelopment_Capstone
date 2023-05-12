from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    # path for about view
    path(route="about.html", view=views.about, name='about'),
    path(route="", view=views.about, name='index'),
    path(route="login.html", view=views.login_request, name='login_request'),
    #bogus route, it just needed to be something
    path(route="logout_request.html", view=views.logout_request, name='logout_request'),
    path(route="logout.html", view=views.logout_final, name='logout_final'),
    path(route="contact.html", view=views.contact, name='contact'),
    path(route="register", view=views.register_request, name='register'),
    path(route="logged_in.html", view=views.logged_in, name='logged_in'),

    path(route="registration.html", view=views.registration, name='registration'),

    path(route='dealerships', view=views.get_dealerships, name='dealerships'),
    path(route="details/<int:dealer_id>/", view=views.get_reviews_for_dealer, name="dealer-details"),
    path(route="reviews/<int:id>/", view=views.add_review, name="reviews"),
    # path for dealer reviews view

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)