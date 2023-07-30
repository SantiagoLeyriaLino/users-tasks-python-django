from django.urls import path
from .views import home, signup, tasks, signout, signin, create_task

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('tasks/', tasks, name='tasks'),
    path('tasks/create/', create_task, name='create_task'),
    path('logout', signout, name='logout'),
    path('signin/', signin, name='signin'),
]