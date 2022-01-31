from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('dashboard', views.dashboard),
    path('logout', views.logout),
    path('add_job', views.add_job),
    path('job_create', views.job_create),
    path('view/<int:job_id>', views.job_details),
    path('claim_job/<int:job_id>', views.claim_job),
    path('edit/<int:job_id>', views.edit),
    path('edit_job/<int:job_id>', views.edit_job),
    path('delete/<int:job_id>', views.delete),
]