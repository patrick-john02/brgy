from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import CustomLoginView, LandingPageView, ErrorPageView

app_name = 'core'

urlpatterns = [
    path('', LandingPageView.as_view(), name='landing'),
    path('Error/', ErrorPageView.as_view(), name='error'),# Landing page for GET
    path('login/', CustomLoginView.as_view(), name='login'),  # Login form handles POST
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)