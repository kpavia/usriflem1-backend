from django.urls import path
from m1.views import VideoListView


urlpatterns = [
    path('v1/videos/', VideoListView.as_view(), name='v1-videos')
]