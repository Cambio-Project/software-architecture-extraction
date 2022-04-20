from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views as views

urlpatterns = [
    path('upload/', csrf_exempt(views.upload)),
    path('export/', views.export_arch),
    path('import/', views.import_arch)
]