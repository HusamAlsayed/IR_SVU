from django.urls import path
from . import views
urlpatterns = [path('', views.questions),
               path('answer', views.answer_question),
               path('seed', views.seeder)]
