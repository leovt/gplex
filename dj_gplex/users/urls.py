from django.urls import include, path
import django.contrib.admin

from users.views import dashboard

urlpatterns = [
    path('accounts/', include('django_registration.backends.activation.urls')),
    path('accounts/', include("django.contrib.auth.urls")),
    path('admin/', django.contrib.admin.site.urls),
    path('dashboard/', dashboard, name='dashboard'),
]
