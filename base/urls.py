from django.urls import path
from . import views  # importing  views of the app-base

urlpatterns = [
    path('home/', views.home, name="home"),  # urls
    path('room/<str:pk>/', views.room, name="room"),

    path('create_room/', views.createRoom, name="createRoom"),

    path('update_room/<str:pk>', views.updateRoom, name="updateRoom"),
    path('delete_room/<str:pk>', views.deleteRoom, name="deleteRoom"),

    # view responses
    path('room_responses/<str:pk>', views.roomResponses, name="roomResponses"),
    path('question_responses/<str:pk>/<str:pk2>', views.questionResponses, name="questionResponses"),
    path('delete_response/<str:pk>/<str:pk2>/<str:pk3>/', views.deleteResponse, name="deleteResponse"),

    path('create_question/<str:pk>', views.createQuestion, name="createQuestion"),
    path('update_question/<str:pk>/<str:pk2>', views.updateQuestion, name="updateQuestion"),
    path('delete_question/<str:pk>/<str:pk2>', views.deleteQuestion, name="deleteQuestion"),

    # unverified rooms
    path('unverified_rooms/', views.unverifiedRooms, name="unverifiedRooms"),
    path('approve/<str:pk>', views.approveRoom, name="approveRoom"),
    path('reject/<str:pk>', views.rejectRoom, name="rejectRoom"),

    # myrooms
    path('myrooms', views.myRooms, name="myRooms"),
    path('myprofile', views.myProfile, name="myProfile"),
    # path('final_submit/', views.finalSubmit, name="finalSubmit"),

    path('verify_user/<str:pk>', views.verifyUser, name="verifyUser"),
]
