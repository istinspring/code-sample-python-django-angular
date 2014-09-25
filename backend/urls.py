from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^api/', include('backend.libs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # route all urls except above to index
    url(r'^.*', include('backend.main.urls')),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
