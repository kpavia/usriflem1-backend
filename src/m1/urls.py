from django.urls import path
from m1.views import (VideoListView, SerialNumberView)


urlpatterns = [
    path('v1/videos/', VideoListView.as_view(), name='v1-videos'),
    path('v1/serial-number/lookup/', SerialNumberView.as_view(), name='v1-serial-lookup')
]
