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
    path(route="", view=views.about, name='about'),
    path(route="login.html", view=views.login, name='login'),
    path(route="logout.html", view=views.logout, name='logout'),
    path(route="contact.html", view=views.contact, name='contact'),

    path(route="registration.html", view=views.registration, name='registration'),
   # path for contact us view

    # path for registration

    # path for login

    # path for logout

    path(route='', view=views.get_dealerships, name='index'),

    # path for dealer reviews view

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)