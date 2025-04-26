from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

app_name = 'community_event'

urlpatterns = [
    # Community Events
    path('events/', views.CommunityEventListView.as_view(), name='event_list'),
    path('events/create/', views.CommunityEventCreateView.as_view(), name='event_create'),

    # Volunteering Opportunities
    path('volunteering/', views.VolunteeringOpportunityListView.as_view(), name='volunteering_list'),
    path('volunteering/create/', views.VolunteeringOpportunityCreateView.as_view(), name='volunteering_create'),

    # Forum
    path('forum/', views.ForumTopicListView.as_view(), name='forum_topic_list'),
    path('forum/create/', views.ForumTopicCreateView.as_view(), name='forum_topic_create'),
    path('forum/post/', views.ForumPostCreateView.as_view(), name='forum_post_create'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)