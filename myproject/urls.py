from django.contrib import admin
from django.urls import path
from videoapp import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home
    path('', views.index, name='home'),

    # ------------------------
    # Airwriting
    # ------------------------
    path('airwriting/', views.airwriting_page, name='airwriting'),
    path('airwriting_video/', views.airwriting_video_feed, name='airwriting_video'),
    path('get_airwriting_result/', views.get_airwriting_result, name='get_airwriting_result'),

    # ------------------------
    # Gesture
    # ------------------------
    path('gesture/', views.gesture_page, name='gesture'),
    path('gesture_video/', views.gesture_video_feed, name='gesture_video'),
    path('get_gesture_result/', views.get_gesture_result, name='get_gesture_result'),
]