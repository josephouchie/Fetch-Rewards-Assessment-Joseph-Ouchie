from django.urls import path
from . import views # import from the current directory

# generates the path to the main function add_spend() in the views.py file
urlpatterns = [
    path('',views.add_spend, name='Add'),
    ]