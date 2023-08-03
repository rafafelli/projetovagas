from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('empregos.urls')),  # adicione essa linha
    path('contas/', include('django.contrib.auth.urls')),
]
