from django.urls import path
from . import views  # importing  views of the app-base

urlpatterns = [
    path('room/<str:pk>/<str:pk2>/', views.question, name="question"),
    # path('room/<str:pk>/<str:pk2>/<str:pk3>', views.question2, name="question2"),
    path('room/<str:pk>/<str:pk2>/run', views.runCode, name="runcode"),

    path('view_response/<str:pk>/<str:pk2>/<str:pk3>/', views.viewResponses, name="viewResponses"),
    path('view_response/<str:pk>/<str:pk2>/<str:pk3>/run', views.runResponse, name="runResponse"),

    path('room/<str:pk>/<str:pk2>/final_submit', views.finalSubmit, name="finalSubmit"),
]
