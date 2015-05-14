import logging

from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Brand, Profile
from .serializers import BrandSerializer, ProfileSerializer


logger = logging.getLogger(__name__)


def index(request):
    return HttpResponse('')


class BrandListView(APIView):

    def get(self, request):
        brand_list = Brand.objects.order_by('created')
        serializer = BrandSerializer(brand_list, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BrandSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.instance = Brand.objects.create(name=serializer.validated_data['name'])
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BrandProfileListView(APIView):

    def get(self, request, brand_id):
        brand = get_object_or_404(Brand, id=brand_id)

        key = 'brands:{}.{}:profiles'.format(brand.id, brand.modified)

        results = cache.get(key)

        if results is None:
            serializer = ProfileSerializer(brand.profiles.order_by('created'), many=True)
            results = serializer.data
            logger.info('CACHE MISS: {}'.format(key))
            cache.set(key, results)
        else:
            logger.info('CACHE HIT: {}'.format(key))

        return Response(results)


class ProfileListView(APIView):

    def post(self, request):
        profile = Profile.objects.create()
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProfileBrandListView(APIView):

    def get(self, request, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)

        key = 'profile:{}.{}:brands'.format(profile.id, profile.modified)

        results = cache.get(key)

        if results is None:
            serializer = BrandSerializer(profile.brands.order_by('created'), many=True)
            results = serializer.data
            logger.info('CACHE MISS: {}'.format(key))
            cache.set(key, results)
        else:
            logger.info('CACHE HIT: {}'.format(key))

        return Response(results)


class ProfileBrandDetailView(APIView):

    def put(self, requets, profile_id, brand_id):
        profile = get_object_or_404(Profile, id=profile_id)
        brand = get_object_or_404(Brand, id=brand_id)

        profile.brands.add(brand)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, requets, profile_id, brand_id):
        profile = get_object_or_404(Profile, id=profile_id)
        brand = get_object_or_404(Brand, id=brand_id)

        profile.brands.remove(brand)

        return Response(status=status.HTTP_204_NO_CONTENT)
