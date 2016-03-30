from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('core.urls')),
    url(r'^elections/', include('elections.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
