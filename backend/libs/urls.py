from django.conf.urls import patterns, url

from backend.libs.api import ModelsList, ModelData

urlpatterns = patterns('',
    url(r'^models$', ModelsList.as_view(), name='models-list'),
    url(r'^models/(?P<name>\w+)$', ModelData.as_view(), name='model-data'),
    url(r'^models/(?P<name>\w+)/item/(?P<pk>\d+)$', ModelData.as_view(), name='model-data'),
)
