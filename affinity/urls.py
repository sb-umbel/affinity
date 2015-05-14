from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^brands$', views.BrandListView.as_view(), name='brand_list'),
    url(r'^brands/(?P<brand_id>[\w-]+)/profiles$', views.BrandProfileListView.as_view(), name='brand_profile_list'),
    url(r'^profiles$', views.ProfileListView.as_view(), name='profile_list'),
    url(r'^profiles/(?P<profile_id>[\w-]+)/brands$', views.ProfileBrandListView.as_view(), name='profile_brand_list'),
    url(r'^profiles/(?P<profile_id>[\w-]+)/brands/(?P<brand_id>[\w-]+)$', views.ProfileBrandDetailView.as_view(), name='profile_brand_detail'),
]
