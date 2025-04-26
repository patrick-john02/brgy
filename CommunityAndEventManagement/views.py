from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from core.mixins import ResidentRequiredMixin
from django.urls import reverse_lazy
from .models import (
    CommunityEvent, VolunteeringOpportunity, VolunteerSignup,
    ForumTopic, ForumPost
)

class CommunityEventListView(LoginRequiredMixin, ResidentRequiredMixin, ListView):
    model = CommunityEvent
    template_name = 'CommunityAndEventManagement/event_list.html'
    context_object_name = 'events'


class CommunityEventCreateView(LoginRequiredMixin, ResidentRequiredMixin, CreateView):
    model = CommunityEvent
    fields = ['title', 'description', 'location', 'start_datetime', 'end_datetime']
    template_name = 'CommunityAndEventManagement/event_form.html'
    success_url = reverse_lazy('community_event:event_list')

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        return super().form_valid(form)

class VolunteeringOpportunityListView(LoginRequiredMixin, ResidentRequiredMixin, ListView):
    model = VolunteeringOpportunity
    template_name = 'CommunityAndEventManagement/volunteering_list.html'
    context_object_name = 'opportunities'


class VolunteeringOpportunityCreateView(LoginRequiredMixin, ResidentRequiredMixin, CreateView):
    model = VolunteeringOpportunity
    fields = ['title', 'description', 'date', 'time', 'location']
    template_name = 'CommunityAndEventManagement/volunteering_form.html'
    success_url = reverse_lazy('community_event:volunteering_list')

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        return super().form_valid(form)

class ForumTopicListView(LoginRequiredMixin, ResidentRequiredMixin, ListView):
    model = ForumTopic
    template_name = 'CommunityAndEventManagement/forum_topic_list.html'
    context_object_name = 'topics'


class ForumTopicCreateView(LoginRequiredMixin, ResidentRequiredMixin, CreateView):
    model = ForumTopic
    fields = ['title', 'description']
    template_name = 'CommunityAndEventManagement/forum_topic_form.html'
    success_url = reverse_lazy('community_event:forum_topic_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class ForumPostCreateView(LoginRequiredMixin, ResidentRequiredMixin, CreateView):
    model = ForumPost
    fields = ['topic', 'content']
    template_name = 'CommunityAndEventManagement/forum_post_form.html'
    success_url = reverse_lazy('community_event:forum_topic_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)